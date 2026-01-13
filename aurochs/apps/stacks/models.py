# import statistics
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

from django.db import models
from reports.models import Report, Scorecard
from frameworks.models import Framework
from organizations.models import User, GenericPermission
from django.utils import timezone
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from utils.helpers import rel
from utils.models import BaseModel, HashidPermissionedModel
from reports.helpers import setup_pdf_worker_thread, generate_pdf_page_worker, add_page


class Stack(HashidPermissionedModel):
    user_specific_caching = True

    name = models.CharField(max_length=1000, null=True)
    subtitle = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    reports = models.ManyToManyField(Report)

    def to_data(self, requesting_user):
        from frameworks.models import Framework

        # stats = {}
        # for f in Framework.authorized_objects.authorize(
        #     user=requesting_user
        # ).findable.filter(pk__in=[f.pk for f in self.frameworks.all()]):
        #     stats[f.id] = {}
        #     stats[f.id]["criteria"] = {}
        #     for c in f.criteria:
        #         scores = [
        #             scs.score
        #             for scs in ScorecardScore.objects.all()
        #             .filter(criteria=c, scorecard__in=self.scorecards)
        #             .exclude(score=None)
        #             .all()
        #         ]
        #         if len(scores) > 1:
        #             stats[f.id]["criteria"][c.id] = {"stddev": statistics.stdev(scores)}
        #         else:
        #             stats[f.id]["criteria"][c.id] = {"stddev": None}

        # if self.can_read(user=requesting_user):
        #     scorecards = [rel(c) for c in self.scorecards]
        # else:
        #     scorecards = [
        #         rel(c) for c in self.scorecards.filter(scorer=requesting_user)
        #     ]

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
            "reports": [
                rel(c)
                for c in Report.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[r.pk for r in self.reports.all()])
            ],
            "comments": [rel(c) for c in self.comments],
            "permissions": self.permissions_dict,
            "subscribed": self.subscribed(requesting_user),
            "tags": [rel(t) for t in self.tags(requesting_user)],
            "search_text": self.search_text(requesting_user),
            # "statistics": stats,
            "subscribers": [rel(u) for u in self.subscribers],
        }

    def child_objects(self, requesting_user):
        from frameworks.models import Framework

        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = []
        objs.extend(
            [
                o
                for o in Report.authorized_objects.authorize(
                    user=requesting_user
                ).findable.filter(pk__in=[r.pk for r in self.reports.all()])
            ]
        )
        objs.extend([o for o in self.comments])
        objs.extend([t for t in self.tags(requesting_user)])
        objs.extend([c.user for c in self.comments])
        objs.extend([c.created_by for c in self.comments])
        objs.extend([s for s in self.subscribers])
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        if requesting_user:
            objs.append(requesting_user)

        return objs

    api_writable_fields = [
        "name",
        "subtitle",
        "notes",
    ]

    def __str__(self):
        return self.name or ""

    @property
    def authorized_reports(self):
        if hasattr(self, "_auth_kwargs") and hasattr(
            getattr(self, "reports"), "authorize"
        ):
            return self.reports.authorize(**self._auth_kwargs).all()

        elif hasattr(self.__class__.authorized_objects, "_auth_kwargs") and hasattr(
            getattr(self, "reports"), "authorize"
        ):
            return self.reports.authorize(
                **self.__class__.authorized_objects._auth_kwargs
            ).all()
        return self.reports.all()

    @property
    def ordered_reports(self):
        return self.authorized_reports.order_by("-ox_score")

    @property
    def frameworks(self):
        r_pks = self.authorized_reports.values_list("id", flat=True)
        scorecard_pks = Scorecard.objects.filter(report_id__in=r_pks).values_list(
            "framework_id", flat=True
        )
        return Framework.objects.filter(pk__in=scorecard_pks)

    @property
    def scorecards(self):
        r_pks = self.authorized_reports.values_list("id", flat=True)
        return Scorecard.objects.filter(report_id__in=r_pks)

    @property
    def average_ox_score(self):
        scores = []
        for r in self.authorized_reports:
            if r.ox_score is not None:
                scores.append(r.ox_score)

        return round(sum(scores) / len(scores))

    def generate_pdf(
        self,
        title=None,
        org_name=None,
        distribution_text=None,
        page_theme=None,
        org_logo=None,
        requesting_user=None,
        page_domain="",
    ):
        from organizations.serializers import OmniSerializer

        MAX_WIDTH = 400
        MAX_HEIGHT = 300
        now = timezone.now()
        frameworks = []
        for f in self.frameworks:
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
        scores_by_criteria_by_report = {}

        for r in self.authorized_reports:
            if r.ox_id not in scores_by_criteria_by_report:
                scores_by_criteria_by_report[r.ox_id] = {}

            for s in r.scorecards:
                for scs in s.scores:
                    if scs.criteria.ox_id not in scores_by_criteria_by_report[r.ox_id]:
                        scores_by_criteria_by_report[r.ox_id][scs.criteria.ox_id] = {
                            "total": 0,
                            "scores": [],
                            "score_values": [],
                            "scores_including_skipped": [],
                            "stddev": -1,
                            "criteria": scs.criteria,
                            "report": r,
                        }
                    scores_by_criteria_by_report[r.ox_id][scs.criteria.ox_id][
                        "scores_including_skipped"
                    ].append(scs)
                    if scs.score is not None:
                        scores_by_criteria_by_report[r.ox_id][scs.criteria.ox_id][
                            "total"
                        ] += scs.score
                        scores_by_criteria_by_report[r.ox_id][scs.criteria.ox_id][
                            "scores"
                        ].append(scs)
                        scores_by_criteria_by_report[r.ox_id][scs.criteria.ox_id][
                            "score_values"
                        ].append(scs.score)

            for c_id in scores_by_criteria_by_report[r.ox_id]:
                scores_by_criteria_by_report[r.ox_id][c_id]["average"] = 0
                if len(scores_by_criteria_by_report[r.ox_id][c_id]["scores"]) > 0:
                    scores_by_criteria_by_report[r.ox_id][c_id][
                        "average"
                    ] = scores_by_criteria_by_report[r.ox_id][c_id]["total"] / len(
                        scores_by_criteria_by_report[r.ox_id][c_id]["scores"]
                    )
                if len(scores_by_criteria_by_report[r.ox_id][c_id]["score_values"]) > 1:
                    scores_by_criteria_by_report[r.ox_id][c_id][
                        "stddev"
                    ] = statistics.stdev(
                        scores_by_criteria_by_report[r.ox_id][c_id]["score_values"]
                    )

        for _, r in scores_by_criteria_by_report.items():
            for c, scs in r.items():
                c_id = scs["criteria"].ox_id
                if c_id not in scores_by_criteria:
                    scores_by_criteria[c_id] = {
                        "total": 0,
                        "scores": [],
                        "score_values": [],
                        "scores_including_skipped": [],
                        "stddev": -1,
                        "report": scs["report"],
                        "criteria": scs["criteria"],
                    }

                scores_by_criteria[scs["criteria"].ox_id][
                    "scores_including_skipped"
                ].append(scs)
                if scs["average"] is not None:
                    scores_by_criteria[scs["criteria"].ox_id]["total"] += scs["average"]
                    scores_by_criteria[scs["criteria"].ox_id]["scores"].append(scs)
                    scores_by_criteria[scs["criteria"].ox_id]["score_values"].append(
                        scs["average"]
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

        # all_sources = self.sources.filter(deleted=False).distinct().all()
        context = {
            "stack_id": self.pk,
            "stack": self,
            # "data": data,
            "scores_by_criteria": scores_by_criteria,
            "author": self.created_by,
            "frameworks": self.frameworks,
            "scorecards": self.scorecards,
            "now": now,
            "title": mark_safe(title or self.name),
            "org_name": mark_safe(org_name),
            "distribution_text": mark_safe(distribution_text.upper()),
            "page_theme": page_theme,
            "org_logo_resized_base64": org_logo_resized_base64,
            "PAGE_DOMAIN": page_domain,
            # "has_sources": len(all_sources) > 0,
            # "all_sources": all_sources,
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
                "stack-cover",
                "pdf/stack-cover.html",
                context,
            ]
        )
        pdf_renders.append(
            [
                "stack-overview",
                "pdf/stack-overview.html",
                context,
            ]
        )

        pdf_renders.append(
            [
                "stack-back",
                "pdf/stack-back.html",
                context,
            ]
        )
        pdf_renders.append(
            [
                "stack-notes",
                "pdf/stack-notes.html",
                context,
            ]
        )
        # if len(all_sources) > 0:
        #     pdf_renders.append(
        #         [
        #             "stack-sources",
        #             "pdf/stack-sources.html",
        #             context,
        #         ]
        #     )

        framework_documents = []
        for f in self.frameworks:
            framework_context = context.copy()
            framework_context["f"] = f
            framework_context["criteria_with_scores"] = []
            for c in f.criteria:
                if not hasattr(c, "scores"):
                    c.scores = []
                for r in self.authorized_reports:
                    for sc in r.scorecards:
                        if sc.framework.pk == f.pk:
                            for scs in sc.scores:
                                if scs.criteria.pk == c.pk:
                                    c.scores.append(scs)
                if len(c.scores) > 0:
                    framework_context["criteria_with_scores"].append(c)

            pdf_renders.append(
                [
                    f"stack-frameworks-{f.pk}",
                    "pdf/stack-framework.html",
                    framework_context,
                ]
            )
            framework_documents.append(f)

            pdf_renders.append(
                [
                    f"stack-comment-{f.pk}",
                    "pdf/stack-comment.html",
                    framework_context,
                ]
            )

        return_dict = {}
        # Parallelize instead, ~2x speedup.
        # We've moved to background workers and celery complains.
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
            result = add_page(return_dict["stack-cover"], result)
            result = add_page(return_dict["stack-overview"], result)
            for f in self.frameworks:
                result = add_page(return_dict[f"stack-frameworks-{f.pk}"], result)

            for f in self.frameworks:
                result = add_page(return_dict[f"stack-comment-{f.pk}"], result)

            # result = add_page(return_dict["stack-frameworks"], result)
            # result = add_page(return_dict["stack-graphs"], result)

            # for s in self.scorecards:
            #     result = add_page(return_dict[f"stack-scorecards-{s.pk}"], result)

            result = add_page(return_dict["stack-notes"], result)
            # if len(all_sources) > 0:
            #     result = add_page(return_dict["stack-sources"], result)
            result = add_page(return_dict["stack-back"], result)

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
            scorecard.report.name,
            scorecard.report.ox_id,
            round(scorecard.report.ox_score),
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
            "Stack Name",
            "Stack ID",
            "Report Name",
            "Report ID",
            "Report Ox Score",
            "Scorer",
        ]

        max_num_criteria = 0
        for rep in self.ordered_reports:
            for sc in rep.scorecards:
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

        for rep in self.ordered_reports:
            for sc in rep.scorecards:
                if len(sc.framework.criteria) > 0:
                    writer.writerow(self._csv_row(sc, max_num_criteria))

        f.seek(0)
        return f.read()
