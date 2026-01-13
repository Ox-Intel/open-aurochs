import base64
import csv
import hashlib
import json
import statistics
from decimal import Decimal
from io import BytesIO, StringIO
from tempfile import SpooledTemporaryFile

from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Avg
from django.utils.functional import cached_property
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

from api.chart_utils.chart_utils import (
    _add_header_footer,
    assemble_ppt,
)
from organizations.models import Organization, Team
from utils.models import (
    BaseModel,
    HashidPermissionedModel,
    PermissionedModel,
    HashidBaseModel,
)
from utils.helpers import rel


class Framework(HashidPermissionedModel):
    user_specific_caching = True

    name = models.TextField(null=True)
    subtitle = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "frameworks.Framework", blank=True, null=True, on_delete=models.SET_NULL
    )

    criteria_hash = models.CharField(max_length=255, null=True)
    gpt_prompt = models.TextField(blank=True, null=True)
    gpt_context = models.TextField(blank=True, null=True)

    api_writable_fields = [
        "name",
        "subtitle",
        "notes",
    ]

    def to_data(self, requesting_user):
        from reports.models import Report, ScorecardScore

        stats = {}
        allowed_scorecards = []
        for r in self.reports:
            allowed_scorecards.extend(r.scorecards)
        for c in self.criteria:
            scores = [
                scs.score
                for scs in ScorecardScore.objects.all()
                .filter(criteria=c, scorecard__in=allowed_scorecards)
                .exclude(score=None)
                .all()
            ]
            if len(scores) > 1:
                stats[c.id] = {"stddev": statistics.stdev(scores)}
            else:
                stats[c.id] = {"stddev": None}

        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "notes": self.notes,
            "created_by": rel(self, "created_by"),
            "modified_by": rel(self, "modified_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            "ox_score": self.ox_score,
            "has_skipped": self.has_skipped,
            "average_feedback_score": self.average_feedback_score,
            "number_of_users": self.number_of_users,
            "number_of_reports": self.number_of_reports,
            "report_id_list": self.report_id_list,
            "highest_scoring_criterion": rel(self, "highest_scoring_criterion"),
            "lowest_scoring_criterion": rel(self, "lowest_scoring_criterion"),
            "criteria": [rel(c) for c in self.criteria],
            "comments": [rel(c) for c in self.comments],
            "permissions": self.permissions_dict,
            "subscribed": self.subscribed(requesting_user),
            "tags": [rel(t) for t in self.tags(requesting_user)],
            "search_text": self.search_text(requesting_user),
            "statistics": stats,
            "subscribers": [rel(u) for u in self.subscribers],
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = []
        objs.extend([c for c in self.criteria.all()])
        objs.extend([c for c in self.comments])
        objs.extend([c.user for c in self.comments])
        objs.extend([t for t in self.tags(requesting_user)])
        objs.extend([c.created_by for c in self.comments])
        objs.extend([s for s in self.subscribers])
        if self.highest_scoring_criterion:
            objs.append(self.highest_scoring_criterion)
        if self.lowest_scoring_criterion:
            objs.append(self.lowest_scoring_criterion)
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.
        from reports.models import Report, Scorecard

        objs = []
        if requesting_user:
            objs.extend(
                [
                    r
                    for r in Scorecard.authorized_objects.authorize(
                        user=requesting_user
                    )
                    .findable.filter(framework=self)
                    .all()
                ]
            )
            objs.append(requesting_user)

        return objs

    def __str__(self):
        return self.name or ""

    def save(self, *args, **kwargs):
        created = True
        if self.pk:
            created = False
            hash_string = ""
            for c in self.criteria:
                hash_string += f"{c.pk}-{c.name} |"
            h = hashlib.new("SHA512")
            h.update(hash_string.encode())
            self.criteria_hash = h.hexdigest()

        super(Framework, self).save(*args, **kwargs)
        if created:
            hash_string = ""
            for c in self.criteria:
                hash_string += f"{c.pk}-{c.name} |"
            h = hashlib.new("SHA512")
            h.update(hash_string.encode())
            self.criteria_hash = h.hexdigest()
            self.save()

    @cached_property
    def ox_score(self):
        total_scores = 0
        num_scores = 0
        for s in self.scorecards:
            if s.ox_score or s.ox_score == 0:
                total_scores += s.ox_score
                num_scores += 1

        if num_scores > 0:
            return Decimal(round(total_scores / num_scores))
        return None

    def report_ox_score(self, report):
        total_scores = 0
        num_scores = 0
        for s in report.scorecards:
            if s.framework == self and (s.ox_score or s.ox_score == 0):
                total_scores += s.ox_score
                num_scores += 1

        if num_scores > 0:
            return Decimal(round(total_scores / num_scores))
        return None

    def stack_ox_score(self, stack):
        scores_by_criteria = {}
        for report in stack.authorized_reports:
            for s in report.scorecards:
                if s.framework == self:
                    for scs in s.scores:
                        if scs.ox_id not in scores_by_criteria:
                            scores_by_criteria[scs.ox_id] = []
                        scores_by_criteria[scs.ox_id].append(scs)

        if len(scores_by_criteria.keys()) > 0:
            total_scores = 0
            max_possible_scores = 0
            for sc_id, scores in scores_by_criteria.items():
                criteria_total = 0
                num_scores = 0
                for s in scores:
                    if s.score is not None:
                        criteria_total += s.score
                        num_scores += 1
            if num_scores > 0:
                total_scores += (criteria_total / num_scores) * s.criteria.weight
                max_possible_scores += 10 * s.criteria.weight
            return Decimal(round(100 * total_scores / max_possible_scores))
        return None

    @cached_property
    def has_skipped(self):
        skips_by_framework = {}
        for s in self.scorecards:
            skips_by_framework[s.framework.ox_id] = True
            if not s.has_skipped:
                skips_by_framework[s.framework.ox_id] = False

        for k, skipped in skips_by_framework.items():
            if skipped:
                return True

        return False

    @cached_property
    def number_of_users(self):
        return self.scorecards.distinct("scorer").count()

    @cached_property
    def number_of_reports(self):
        return self.reports.count()

    @cached_property
    def average_feedback_score(self):
        from reports.models import Report, Scorecard

        total_scores = 0
        num_scores = 0
        report_ids = Scorecard.objects.filter(framework=self).values_list(
            "report_id", flat=True
        )
        for r in Report.raw_objects.filter(id__in=report_ids).exclude(
            feedback_score=None
        ):
            total_scores += r.feedback_score
            num_scores += 1

        if num_scores > 0:
            return Decimal(total_scores / num_scores)
        return None

    @property
    def criteria(self):
        return (
            self.criteria_set.exclude(deleted=True)
            .all()
            .order_by(
                "id",
            )
        )

    @cached_property
    def criteria_with_averages(self):
        return [(c, c.average_score) for c in self.criteria]

    @cached_property
    def highest_scoring_criterion(self):
        highest_score = -1
        criterion = None
        for c, score in self.criteria_with_averages:
            if score and score > highest_score:
                highest_score = score
                criterion = c
        return criterion

    @cached_property
    def lowest_scoring_criterion(self):
        lowest_score = 999999
        criterion = None
        for c, score in self.criteria_with_averages:
            if score and score < lowest_score:
                lowest_score = score
                criterion = c
        return criterion

    @property
    def reports(self):
        from reports.models import Report, Scorecard

        report_ids = Scorecard.objects.filter(framework=self).values_list(
            "report_id", flat=True
        )
        if hasattr(self, "_auth_kwargs"):
            return (
                Report.authorized_objects.authorize(**self._auth_kwargs)
                .findable.filter(id__in=report_ids)
                .all()
            )

        elif hasattr(self.__class__.authorized_objects, "_auth_kwargs"):
            return (
                Report.authorized_objects.authorize(
                    **self.__class__.authorized_objects._auth_kwargs
                )
                .findable.filter(id__in=report_ids)
                .all()
            )
        return Report.raw_objects.filter(id__in=report_ids).exclude(deleted=True)

    @property
    def all_reports(self):
        from reports.models import Report, Scorecard

        report_ids = Scorecard.objects.filter(framework=self).values_list(
            "report_id", flat=True
        )
        return Report.objects.filter(id__in=report_ids).all()

    @cached_property
    def report_id_list(self):
        return [i for i in self.reports.values_list("pk", flat=True)]

    @property
    def num_reports(self):
        return self.reports.count()

    @cached_property
    def scorecards(self):
        return self.scorecard_set.exclude(deleted=True).all()

    def framework_export(self, file_type: str, pdf_mode: bool = False):
        # pio.kaleido.scope.chromium_args += ("--disable-gpu-sandbox",)
        # pio.kaleido.scope.chromium_args += ("--single-process",)
        output_list = []

        # values = [criteria.weight for criteria in self.criteria]
        # labels = [criteria.name for criteria in self.criteria]

        title = self.name

        # if file_type == "png" and pdf_mode:
        #     return make_donut_chart(
        #         values=values, labels=labels, include_labels=False, include_legend=False
        #     )

        # donut_chart = make_donut_chart(values=values, labels=labels)

        png_bytes_output = BytesIO()
        # donut_chart.write_image(png_bytes_output)

        if file_type == "ppt" and not pdf_mode:
            branded_chart_image = _add_header_footer(
                image_bytes=png_bytes_output,
                include_title=False,
            )

            output_list.append(dict(image=branded_chart_image, title=title))
            prs = assemble_ppt(image_list=output_list)
            ppt_bytes_output = BytesIO()
            prs.save(ppt_bytes_output)
            ppt_bytes_output.seek(0)
            return ppt_bytes_output

        if file_type == "png" and not pdf_mode:
            branded_png_image = _add_header_footer(
                image_bytes=png_bytes_output,
                include_title=True,
                title=title,
            )

            return branded_png_image

    def _csv_row(self, scorecard, num_criteria):
        ret = [
            scorecard.framework.name,
            scorecard.framework.ox_id,
        ]
        count = 1
        for c in scorecard.framework.criteria:
            ret += [c.ox_id, c.name, c.description, c.weight]
            count += 1
        while count < num_criteria:
            ret += ["", "", "", ""]
            count += 1

        ret += [
            scorecard.report.name,
            scorecard.report.ox_id,
            scorecard.report.subtitle,
            scorecard.report.feedback_score,
            scorecard.report.feedback_comment,
            # "N/A",
            # scorecard.report.ox_score,
        ]
        count = 1
        for c in scorecard.scores:
            if c.score:
                ret += [
                    round(c.score),
                    c.comment,
                ]
            else:
                ret += [
                    c.score,
                    c.comment,
                ]
            count += 1

        while count < num_criteria:
            ret += [
                "",
                "",
            ]
            count += 1

        ret += [
            scorecard.scorer.full_name,
            scorecard.ox_score,
        ]
        return ret

    @property
    def csv_export(self):
        f = StringIO()
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        headers = [
            "Framework Name",
            "Framework ID",
        ]

        count = 1
        criteria_list = [
            None,
        ]
        for c in self.criteria:
            headers += (
                f"Criteria {count} ID",
                f"Criteria {count} name",
                f"Criteria {count} description",
                f"Criteria {count} weight",
            )
            criteria_list.append(c)
            count += 1
        num_criteria = count

        headers += (
            "Report Name",
            "Report ID",
            "Summary",
            "Outcome Score",
            "Outcome Comment",
        )
        # headers += ["Report Ox Score", ]
        count = 1
        for c in self.criteria:
            headers += (
                f"Score - Criteria {count} - {c.name} ",
                f"Comment - Criteria {count} - {c.name} ",
            )
            count += 1

        headers += [
            "Scorecard scorer",
            "Scorecard Ox Score",
        ]
        writer.writerow(headers)

        for r in self.reports:
            for s in r.scorecards:
                if len(s.framework.criteria) > 0:
                    writer.writerow(self._csv_row(s, num_criteria))

        f.seek(0)
        return f.read()


class Criteria(HashidBaseModel):
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    weight = models.DecimalField(blank=True, null=True, decimal_places=1, max_digits=4)
    index = models.IntegerField(blank=True, null=True)

    def to_data(self, requesting_user):
        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "name": self.name,
            "description": self.description,
            # "framework": rel(self, "framework"),
            "weight": self.weight,
            "index": self.index,
            "relative_weight_as_percent": self.relative_weight_as_percent,
            "relative_weight_as_percent_of_max": self.relative_weight_as_percent_of_max,
            "average_score": self.average_score,
            "framework_pk": self.framework_pk,
            "created_by": rel(self, "created_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            "my_average_score": self.user_average_score(requesting_user),
        }

    # def save(self, *args, **kwargs):
    #     print(self.index)
    #     print(self.framework)
    #     print(self.framework.criteria_set)
    #     if not self.index and self.index != 0:
    #         print(self.framework.criteria_set.exclude(index=None).count())
    #         if self.framework.criteria_set.exclude(index=None).count() > 0:
    #             self.index = (
    #                 self.framework.criteria_set.exclude(index=None)
    #                 .order_by("-index")[0]
    #                 .index
    #                 + 1
    #             )
    #         else:
    #             self.index = 0
    #     super(Criteria, self).save(*args, **kwargs)

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = []
        objs.append(self.framework)
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        objs.append(self.framework)
        if requesting_user:
            objs.append(requesting_user)

        return objs

    api_writable_fields = [
        "name",
        "description",
        "weight",
        "index",
    ]

    def __str__(self):
        return f"{self.name} - {self.framework}" or ""

    @cached_property
    def framework_pk(self):
        return self.framework.pk

    @cached_property
    def relative_weight_as_percent(self):
        if not self.weight:
            return 0

        total_weights = 0
        for c in self.framework.criteria.all():
            if c.weight:
                total_weights += c.weight
        if total_weights > 0:
            return Decimal(100 * self.weight / total_weights)
        return 0

    @cached_property
    def relative_weight_as_percent_of_max(self):
        if not self.weight:
            return 0

        largest_weight = 0
        for c in self.framework.criteria.all():
            if c.weight > largest_weight:
                largest_weight = c.weight
        if largest_weight > 0:
            return Decimal(100 * self.weight / largest_weight)
        return 0

    @cached_property
    def average_score(self):
        from reports.models import ScorecardScore

        scores = (
            ScorecardScore.objects.filter(criteria=self)
            .exclude(score=None)
            .aggregate(Avg("score"))
        )
        if "score__avg" in scores:
            return scores["score__avg"]
        return None

    def user_average_score(self, requesting_user):
        from reports.models import ScorecardScore

        scores = (
            ScorecardScore.objects.filter(
                criteria=self, scorecard__scorer=requesting_user
            )
            .exclude(score=None)
            .aggregate(Avg("score"))
        )
        if "score__avg" in scores:
            return scores["score__avg"]
        return None


@receiver(post_save, sender=Framework)
def framework_saved(sender, instance, created, **kwargs):
    from reports.models import Scorecard

    for sc in Scorecard.objects.filter(framework=instance):
        sc.save()


@receiver(post_save, sender=Criteria)
def criteria_saved(sender, instance, created, **kwargs):
    from reports.models import ScorecardScore

    for scs in ScorecardScore.objects.filter(criteria=instance):
        scs.save()
