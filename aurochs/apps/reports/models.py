import csv
import chompjs
import fitz
import statistics
from delta import html
from decimal import Decimal
from django.core.files.temp import NamedTemporaryFile
from io import BytesIO, StringIO
from tempfile import SpooledTemporaryFile
from PIL import Image, ImageOps, ImageDraw, ImageFont
import base64
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

from api.chart_utils.chart_utils import (
    _add_header_footer,
    assemble_ppt,
)
from django.db import models
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.functional import cached_property
from django.dispatch import receiver
from django.db.models.signals import post_save
from frameworks.models import Framework, Criteria
from organizations.models import User, GenericPermission
from reports.helpers import setup_pdf_worker_thread, generate_pdf_page_worker, add_page
from sources.models import Source
from utils.helpers import rel
from utils.models import BaseModel, HashidPermissionedModel, HashidBaseModel
from weasyprint import HTML


class Report(HashidPermissionedModel):
    user_specific_caching = True

    name = models.CharField(max_length=1000, null=True)
    subtitle = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    ox_score = models.DecimalField(
        blank=True, null=True, decimal_places=1, max_digits=5
    )
    has_skipped = models.BooleanField(default=False)

    feedback_score = models.DecimalField(
        blank=True, null=True, decimal_places=1, max_digits=5
    )
    feedback_comment = models.TextField(blank=True, null=True)

    sources = models.ManyToManyField(Source, blank=True)
    gpt_prompt = models.TextField(blank=True, null=True)
    gpt_context = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        created = True
        if self.pk:
            created = False
            self.ox_score = self.compute_ox_score()
            self.has_skipped = self.compute_has_skipped()
        super(Report, self).save(*args, **kwargs)
        if created:
            self.ox_score = self.compute_ox_score()
            self.has_skipped = self.compute_has_skipped()
            self.save()

    def to_data(self, requesting_user):
        from frameworks.models import Framework
        from stacks.models import Stack

        stats = {}
        for f in Framework.authorized_objects.authorize(
            user=requesting_user
        ).findable.filter(pk__in=[f.pk for f in self.frameworks]):
            stats[f.id] = {}
            stats[f.id]["criteria"] = {}
            for c in f.criteria:
                scores = [
                    scs.score
                    for scs in ScorecardScore.objects.all()
                    .filter(criteria=c, scorecard__in=self.scorecards)
                    .exclude(score=None)
                    .all()
                ]
                if len(scores) > 1:
                    stats[f.id]["criteria"][c.id] = {"stddev": statistics.stdev(scores)}
                else:
                    stats[f.id]["criteria"][c.id] = {"stddev": None}

        if self.can_read(user=requesting_user):
            scorecards = [rel(c) for c in self.scorecards]
        else:
            scorecards = [
                rel(c) for c in self.scorecards.filter(scorer=requesting_user)
            ]

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
            "feedback_score": self.feedback_score,
            "feedback_comment": self.feedback_comment,
            "frameworks": [
                rel(c)
                for c in Framework.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[f.pk for f in self.frameworks])
            ],
            "sources": [
                rel(c)
                for c in Source.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[s.pk for s in self.sources.all()])
            ],
            "stack_ids": [
                f"{s.ox_id}"
                for s in Stack.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[s.pk for s in self.stack_set.all()])
            ],
            "scorecards": scorecards,
            "comments": [rel(c) for c in self.comments],
            "permissions": self.permissions_dict,
            "subscribed": self.subscribed(requesting_user),
            "tags": [rel(t) for t in self.tags(requesting_user)],
            "search_text": self.search_text(requesting_user),
            "statistics": stats,
            "subscribers": [rel(u) for u in self.subscribers],
        }

    def child_objects(self, requesting_user):
        from frameworks.models import Framework
        from stacks.models import Stack

        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = []
        objs.extend(
            [
                o
                for o in Framework.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[f.pk for f in self.frameworks])
            ]
        )
        objs.extend(
            [
                o
                for o in Source.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[s.pk for s in self.sources.all()])
            ]
        )
        objs.extend(
            [
                c
                for c in Stack.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[s.pk for s in self.stack_set.all()])
            ]
        )
        objs.extend([o for o in self.scorecards])
        objs.extend([o for o in self.comments])
        objs.extend([t for t in self.tags(requesting_user)])
        objs.extend([c.user for c in self.comments])
        objs.extend([c.created_by for c in self.comments])
        objs.extend([s for s in self.subscribers])
        for sc in self.scorecards:
            objs.append(sc)
            objs.append(sc.scorer)
            objs.append(sc.created_by)
            for scs in sc.scores:
                objs.append(scs)
                objs.append(scs.criteria)
                objs.append(scs.created_by)
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        if requesting_user:
            objs.append(requesting_user)
        objs.extend([f for f in self.frameworks])

        return objs

    api_writable_fields = [
        "name",
        "subtitle",
        "notes",
        "feedback_score",
        "feedback_comment",
    ]

    def __str__(self):
        return self.name or ""

    @cached_property
    def color_index(self):
        return self.id % 21

    @cached_property
    def frameworks(self):
        framework_list = []
        for sc in self.scorecards:
            if sc.framework not in framework_list:
                framework_list.append(sc.framework)
        return framework_list

    @property
    def scorecards(self):
        return (
            self.scorecard_set.exclude(deleted=True)
            .distinct()
            .all()
            .order_by("-modified_at")
        )

    def stacks(self, requesting_user):
        from stacks.models import Stack

        return (
            Stack.authorized_objects.authorize(user=requesting_user)
            .filter(reports=self)
            .distinct()
            .order_by("-modified_at")
            .all()
        )

    def compute_ox_score(self):
        total_scores = Decimal(0)
        num_scores = Decimal(0)
        total_possible = Decimal(0)
        criteria_totals = {}
        criteria_weights = {}
        criteria_num_scores = {}
        for s in self.scorecards:
            for sc in s.scores:
                if sc.score is not None:
                    # print(sc)
                    if f"{sc.criteria.pk}" not in criteria_totals:
                        criteria_totals[f"{sc.criteria.pk}"] = 0
                    if f"{sc.criteria.pk}" not in criteria_num_scores:
                        criteria_num_scores[f"{sc.criteria.pk}"] = 0
                    criteria_totals[f"{sc.criteria.pk}"] += sc.score
                    criteria_weights[f"{sc.criteria.pk}"] = sc.weight
                    criteria_num_scores[f"{sc.criteria.pk}"] += 1
                    num_scores += 1
                else:
                    criteria_weights[f"{sc.criteria.pk}"] = sc.weight
            # if s.ox_score or s.ox_score == 0:
            #     total_scores += s.ox_score

        for k, v in criteria_weights.items():
            if k in criteria_totals:
                total_scores += (
                    criteria_totals[k] / criteria_num_scores[k]
                ) * criteria_weights[k]
                total_possible += 10 * criteria_weights[k]
            else:
                total_scores += 0
                total_possible += 10 * criteria_weights[k]

        if total_possible > 0:
            # print(self)
            # print(total_scores)
            # print(total_possible)
            return Decimal(round(Decimal(100) * total_scores / total_possible))
            # todo
        return None

    def compute_has_skipped(self):
        criteria_weights = {}
        criteria_num_scores = {}
        for s in self.scorecards:
            for sc in s.scores:
                if sc.score is not None:
                    criteria_weights[f"{sc.criteria.pk}"] = sc.weight
                    criteria_num_scores[f"{sc.criteria.pk}"] = 1
                else:
                    criteria_weights[f"{sc.criteria.pk}"] = sc.weight

        for k, v in criteria_weights.items():
            if k not in criteria_num_scores:
                return True
        return False

    @property
    def framework_id(self):
        if self.frameworks:
            return [f.pk for f in self.authorized_frameworks]
        return []

    @property
    def authorized_frameworks(self):
        return self.frameworks
        # if hasattr(self, "_auth_kwargs") and hasattr(
        #     getattr(self, "frameworks"), "authorize"
        # ):
        #     return self.frameworks.authorize(**self._auth_kwargs).all()

        # elif hasattr(self.__class__.authorized_objects, "_auth_kwargs") and hasattr(
        #     getattr(self, "frameworks"), "authorize"
        # ):
        #     return self.frameworks.authorize(
        #         **self.__class__.authorized_objects._auth_kwargs
        #     ).all()
        # return self.frameworks.all()

    @property
    def authorized_sources(self):
        if hasattr(self, "_auth_kwargs") and hasattr(
            getattr(self, "sources"), "authorize"
        ):
            return self.sources.authorize(**self._auth_kwargs).all()

        elif hasattr(self.__class__.authorized_objects, "_auth_kwargs") and hasattr(
            getattr(self, "sources"), "authorize"
        ):
            return self.sources.authorize(
                **self.__class__.authorized_objects._auth_kwargs
            ).all()
        return self.sources.all()

    def report_export(self, file_type="png", framework=None, pdf_mode=False):
        # TODO: cruft, clean this up.
        return

    def generate_pdf(
        self,
        title=None,
        org_name=None,
        distribution_text=None,
        page_theme=None,
        org_logo=None,
        requesting_user=None,
        request=None,
        page_domain="",
    ):
        from organizations.serializers import OmniSerializer

        MAX_WIDTH = 400
        MAX_HEIGHT = 300
        now = timezone.now()
        frameworks = []
        for f in self.authorized_frameworks:
            frameworks.append(
                {
                    "framework": f,
                }
            )
        if not org_name:
            ct = ContentType.objects.get_for_model(self)
            gps = GenericPermission.objects.filter(
                object_id=self.pk, content_type=ct
            ).exclude(organization=None)
            for gp in gps:
                if gp in requesting_user.organizations:
                    org_name = gp.organization.name
            if gps.count() == 0:
                for o in requesting_user.organizations:
                    org_name = o.name
                    break

        org_logo_resized_base64 = None
        if org_logo:
            with BytesIO() as f:
                im = Image.open(org_logo).convert("RGBA")

                scale_by_height = False
                if im.height > im.width:
                    new_width = round(im.width * (MAX_HEIGHT / im.height))
                    if new_width > MAX_WIDTH:
                        scale_by_height = True
                    else:
                        im = im.resize((new_width, MAX_HEIGHT))
                else:
                    scale_by_height = True

                if scale_by_height:
                    new_height = round(im.height * (MAX_WIDTH / im.width))
                    im = im.resize((MAX_WIDTH, new_height))

                im.save(f, format="PNG", quality=100)
                f.seek(0)
                org_logo_resized_base64 = base64.b64encode(f.read()).decode("utf-8")

        scores_by_criteria = {}
        for s in self.scorecards:
            for scs in s.scores:
                if scs.criteria.ox_id not in scores_by_criteria:
                    scores_by_criteria[scs.criteria.ox_id] = {
                        "total": 0,
                        "scores": [],
                        "score_values": [],
                        "scores_including_skipped": [],
                        "stddev": -1,
                    }
                scores_by_criteria[scs.criteria.ox_id][
                    "scores_including_skipped"
                ].append(scs)
                if scs.score is not None:
                    scores_by_criteria[scs.criteria.ox_id]["total"] += scs.score
                    scores_by_criteria[scs.criteria.ox_id]["scores"].append(scs)
                    scores_by_criteria[scs.criteria.ox_id]["score_values"].append(
                        scs.score
                    )

        for c_id in scores_by_criteria:
            scores_by_criteria[c_id]["average"] = 0
            if len(scores_by_criteria[c_id]["scores"]) > 0:
                scores_by_criteria[c_id]["average"] = scores_by_criteria[c_id][
                    "total"
                ] / len(scores_by_criteria[c_id]["scores"])
            if len(scores_by_criteria[c_id]["score_values"]) > 1:
                scores_by_criteria[c_id]["stddev"] = statistics.stdev(
                    scores_by_criteria[c_id]["score_values"]
                )

        all_sources = self.sources.filter(deleted=False).distinct().all()
        context = {
            "report_id": self.pk,
            "report": self,
            # "data": data,
            "scores_by_criteria": scores_by_criteria,
            "author": self.created_by,
            "frameworks": self.authorized_frameworks,
            "scorecards": self.scorecards,
            "feedback_score": self.feedback_score,
            "ox_score": self.ox_score,
            "has_skipped": self.has_skipped,
            "now": now,
            "title": mark_safe(title or self.name),
            "org_name": mark_safe(org_name),
            "distribution_text": mark_safe(distribution_text.upper()),
            "page_theme": page_theme,
            "org_logo_resized_base64": org_logo_resized_base64,
            "PAGE_DOMAIN": page_domain,
            "has_sources": len(all_sources) > 0,
            "all_sources": all_sources,
        }

        context["notes"] = mark_safe("")
        try:
            if self.notes:
                if "ops:" in self.notes:
                    ops = chompjs.parse_js_object(self.notes)["ops"]
                else:
                    ops = [
                        {"insert": self.notes},
                    ]
                context["notes"] = mark_safe(html.render(ops))
            else:
                context["notes"] = mark_safe("")
        except:
            # print(self.notes)
            # import traceback
            # traceback.print_exc()
            pass

        context["feedback_comment"] = mark_safe("")
        try:
            if self.feedback_comment:
                if "ops:" in self.feedback_comment:
                    ops = chompjs.parse_js_object(self.feedback_comment)["ops"]
                else:
                    ops = [
                        {"insert": self.feedback_comment},
                    ]
                context["feedback_comment"] = mark_safe(html.render(ops))
            else:
                context["feedback_comment"] = mark_safe("")
        except:
            # print(self.notes)
            # import traceback
            # traceback.print_exc()
            pass

        # If want page numbers, we'll need to add them to the template, render once to see the length,
        # then re-render with the page numbers and overrides. Skipping for now, but FYI for future dev.
        # See: https://github.com/Kozea/WeasyPrint/issues/809

        pdf_renders = []
        pdf_renders.append(
            [
                "report-cover",
                "pdf/report-cover.html",
                context,
            ]
        )
        pdf_renders.append(
            [
                "report-overview",
                "pdf/report-overview.html",
                context,
            ]
        )

        pdf_renders.append(
            [
                "report-back",
                "pdf/report-back.html",
                context,
            ]
        )
        pdf_renders.append(
            [
                "report-notes",
                "pdf/report-notes.html",
                context,
            ]
        )
        if len(all_sources) > 0:
            pdf_renders.append(
                [
                    "report-sources",
                    "pdf/report-sources.html",
                    context,
                ]
            )

        # scorecard_documents = []
        # for s in self.scorecards:
        #     scorecard_context = context.copy()
        #     scorecard_context["scorecard"] = s
        #     pdf_renders.append(
        #         [
        #             f"report-scorecards-{s.pk}",
        #             "pdf/report-scorecard.html",
        #             scorecard_context,
        #         ]
        #     )
        #     scorecard_documents.append(s)

        framework_documents = []
        for f in self.frameworks:
            framework_context = context.copy()
            framework_context["f"] = f

            pdf_renders.append(
                [
                    f"report-frameworks-{f.pk}",
                    "pdf/report-framework.html",
                    framework_context,
                ]
            )
            framework_documents.append(f)

            pdf_renders.append(
                [
                    f"report-comment-{f.pk}",
                    "pdf/report-comment.html",
                    framework_context,
                ]
            )

        return_dict = {}
        # Parallelize instead, ~2x speedup.
        # PARALLELIZE = True
        PARALLELIZE = False
        if not PARALLELIZE:
            for p in pdf_renders:
                return_dict[p[0]] = generate_pdf_page_worker(*p)
        else:
            with ProcessPoolExecutor(
                max_workers=6, initializer=setup_pdf_worker_thread
            ) as executor:
                futures = [
                    (args[0], executor.submit(generate_pdf_page_worker, *args))
                    for args in pdf_renders
                ]
                for key, x in futures:
                    return_dict[key] = x.result()
                executor.shutdown()

        # Combine all reports
        with NamedTemporaryFile(suffix=".pdf") as return_file:
            result = fitz.open()
            result = add_page(return_dict["report-cover"], result)
            result = add_page(return_dict["report-overview"], result)
            for f in self.frameworks:
                result = add_page(return_dict[f"report-frameworks-{f.pk}"], result)

            for f in self.frameworks:
                result = add_page(return_dict[f"report-comment-{f.pk}"], result)

            # result = add_page(return_dict["report-frameworks"], result)
            # result = add_page(return_dict["report-graphs"], result)

            # for s in self.scorecards:
            #     result = add_page(return_dict[f"report-scorecards-{s.pk}"], result)

            result = add_page(return_dict["report-notes"], result)
            if len(all_sources) > 0:
                result = add_page(return_dict["report-sources"], result)
            result = add_page(return_dict["report-back"], result)

            result.save(return_file.name)
            with open(return_file.name, "rb") as ret_f:
                ret_f.seek(0)
                return ret_f.read()

            return_file.seek(0)
            return return_file.read()

    def _csv_row(self, scorecard, num_criteria):
        ret = [
            self.name,
            self.ox_id,
            round(self.ox_score),
            scorecard.scorer.full_name,
            scorecard.framework.name,
            scorecard.framework.ox_id,
            round(scorecard.ox_score),
        ]

        count = 1
        # for c in scorecard.framework.criteria:
        for scs in scorecard.scores:
            score = "Unscored"
            if scs.score:
                score = round(scs.score)
            ret += [
                scs.criteria.ox_id,
                scs.criteria.name,
                scs.criteria.description,
                scs.criteria.weight,
                score,
                scs.comment,
            ]
            count += 1
        while count < num_criteria:
            ret += ["", "", "", ""]
            count += 1

        return ret

    @property
    def csv_export(self):
        f = StringIO()
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        headers = [
            "Report Name",
            "Report ID",
            "Report Ox Score",
            "Scorer",
        ]

        max_num_criteria = 0
        for sc in self.scorecards:
            if len(sc.framework.criteria) > max_num_criteria:
                max_num_criteria = len(sc.framework.criteria)

        headers += (
            "Scorecard Framework Name",
            "Scorecard Framework ID",
            "Scorecard Ox Score",
        )
        for i in range(0, max_num_criteria):
            headers += (
                f"Criteria {i + 1} ID",
                f"Criteria {i + 1} name",
                f"Criteria {i + 1} description",
                f"Criteria {i + 1} weight",
                f"Score - Criteria {i + 1}",
                f"Comment - Criteria {i + 1}",
            )

        writer.writerow(headers)

        for sc in self.scorecards:
            if len(sc.framework.criteria) > 0:
                writer.writerow(self._csv_row(sc, max_num_criteria))

        f.seek(0)
        return f.read()


class Scorecard(HashidBaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    scorer = models.ForeignKey(User, on_delete=models.CASCADE)
    framework_criteria_hash = models.CharField(max_length=255, blank=True, null=True)

    ox_score = models.DecimalField(
        blank=True, null=True, decimal_places=1, max_digits=5
    )
    has_skipped = models.BooleanField(default=False)
    gpt_prompt = models.TextField(blank=True, null=True)
    gpt_context = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        created = True
        if self.pk:
            created = False
            self.ox_score = self.compute_ox_score()
            self.has_skipped = self.compute_has_skipped()
        super(Scorecard, self).save(*args, **kwargs)
        if created:
            self.ox_score = self.compute_ox_score()
            self.has_skipped = self.compute_has_skipped()
            self.save()

    def to_data(self, requesting_user):
        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "framework_criteria_hash": self.framework_criteria_hash,
            "created_by": rel(self, "created_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            "ox_score": self.ox_score,
            "has_skipped": self.has_skipped,
            "scores": [rel(scs) for scs in self.scores],
            "report_pk": self.report.pk,
            "framework_pk": self.framework.pk,
            "scorer": rel(self, "scorer"),
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = [
            self.report,
            self.framework,
            self.scorer,
        ]
        objs.append(self.created_by)
        objs.extend([scs for scs in self.scores])
        objs.extend([scs.criteria for scs in self.scores])
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        objs.append(self.report)
        objs.append(self.framework)
        objs.append(self.scorer)

        if requesting_user:
            objs.append(requesting_user)

        return objs

    def compute_ox_score(self):
        total_scores = 0
        max_scores = 0
        for s in self.scores:
            if s.score is not None:
                total_scores += s.score * s.weight
            max_scores += 10 * s.weight
        if max_scores > 0:
            return Decimal(round(Decimal(100) * total_scores / max_scores))
        return None

    def compute_has_skipped(self):
        for s in self.scores:
            if s.score is None and s.score != 0:
                return True

        return False

    @property
    def report_pk(self):
        return self.report.pk

    @property
    def framework_pk(self):
        return self.framework.pk

    @property
    def scores(self):
        return (
            self.scorecardscore_set.exclude(deleted=True)
            .all()
            .order_by(
                "criteria_id",
                "pk",
            )
        )

    def __str__(self):
        return f"{self.scorer} - {self.report} - {self.framework}"

    def generate_pdf(
        self,
        title=None,
        org_name=None,
        distribution_text=None,
        page_theme=None,
        org_logo=None,
        requesting_user=None,
        request=None,
    ):
        from organizations.serializers import OmniSerializer

        now = timezone.now()

        scores_by_criteria = {}
        for scs in self.scores:
            if scs.criteria.ox_id not in scores_by_criteria:
                scores_by_criteria[scs.criteria.ox_id] = {
                    "total": 0,
                    "scores": [],
                    "score_values": [],
                    "scores_including_skipped": [],
                    "stddev": -1,
                }
            scores_by_criteria[scs.criteria.ox_id]["scores_including_skipped"].append(
                scs
            )
            if scs.score is not None:
                scores_by_criteria[scs.criteria.ox_id]["total"] += scs.score
                scores_by_criteria[scs.criteria.ox_id]["scores"].append(scs)
                scores_by_criteria[scs.criteria.ox_id]["score_values"].append(scs.score)

        for c_id in scores_by_criteria:
            scores_by_criteria[c_id]["average"] = 0
            if len(scores_by_criteria[c_id]["scores"]) > 0:
                scores_by_criteria[c_id]["average"] = scores_by_criteria[c_id][
                    "total"
                ] / len(scores_by_criteria[c_id]["scores"])
            if len(scores_by_criteria[c_id]["score_values"]) > 1:
                scores_by_criteria[c_id]["stddev"] = statistics.stdev(
                    scores_by_criteria[c_id]["score_values"]
                )

        context = {
            "report_id": self.report.ox_id,
            "scorecard": self,
            "report": self.report,
            # "data": data,
            "scores_by_criteria": scores_by_criteria,
            "author": self.created_by,
            "has_skipped": self.has_skipped,
            "now": now,
            "PAGE_DOMAIN": request.build_absolute_uri("/")[:-1],
        }

        pdf_renders = []
        pdf_renders.append(
            [
                "report-scorecard",
                "pdf/report-scorecard.html",
                context,
            ]
        )

        return_dict = {}
        # Parallelize instead, ~2x speedup.
        PARALLELIZE = True
        # PARALLELIZE = False
        if not PARALLELIZE:
            for p in pdf_renders:
                return_dict[p[0]] = generate_pdf_page_worker(*p)
        else:
            with ProcessPoolExecutor(
                max_workers=6, initializer=setup_pdf_worker_thread
            ) as executor:
                futures = [
                    (args[0], executor.submit(generate_pdf_page_worker, *args))
                    for args in pdf_renders
                ]
                for key, x in futures:
                    return_dict[key] = x.result()
                executor.shutdown()

        # Combine all reports
        with NamedTemporaryFile(suffix=".pdf") as return_file:
            result = fitz.open()
            result = add_page(return_dict["report-scorecard"], result)

            result.save(return_file.name)
            with open(return_file.name, "rb") as ret_f:
                ret_f.seek(0)
                return ret_f.read()

            return_file.seek(0)
            return return_file.read()


class ScorecardScore(HashidBaseModel):
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)

    score = models.DecimalField(blank=True, null=True, decimal_places=1, max_digits=4)
    comment = models.TextField(blank=True, null=True)
    gpt_score = models.DecimalField(
        blank=True, null=True, decimal_places=1, max_digits=4
    )
    gpt_scored_last = models.BooleanField(default=False)

    def to_data(self, requesting_user):
        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "weight": self.weight,
            "score": self.score,
            "comment": self.comment,
            "gpt_scored_last": self.gpt_scored_last,
            "scorecard_pk": self.scorecard_pk,
            "scorer": rel(self.scorecard, "scorer"),
            "created_by": rel(self, "created_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            # "scorecard": rel(self, "scorecard"),
            "criteria": rel(self, "criteria"),
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = [
            self.scorecard,
            self.criteria,
        ]
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        objs.append(self.scorecard)
        if requesting_user:
            objs.append(requesting_user)

        return objs

    @cached_property
    def weight(self):
        return self.criteria.weight

    @cached_property
    def scorecard_pk(self):
        return self.scorecard.pk

    def __str__(self):
        return f"{self.scorecard} - {self.criteria}"


@receiver(post_save, sender=ScorecardScore)
def scorecardscore_saved(sender, instance, created, **kwargs):
    instance.scorecard.save()


@receiver(post_save, sender=Scorecard)
def scorecard_saved(sender, instance, created, **kwargs):
    instance.report.save()
