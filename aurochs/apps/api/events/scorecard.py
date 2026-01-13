from api.events.base import BaseEventHandler
from frameworks.models import Framework, Criteria
from reports.models import Report, Scorecard, ScorecardScore
from organizations.models import Organization, Team, User


class CreateScorecardHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # {
        #     "report_id": 5,
        #     "framework_id": 24,
        #     "scores": [
        #         {
        #             "criteria_id": 21,
        #             "comment": "Foo bar",
        #             "score": 5,
        #         },
        #         {
        #             "criteria_id": 22,
        #             "comment": "Ack",
        #             "score": 2,
        #         },
        #     ]
        # }

        r = Report.authorized_objects.authorize(user=request.user).scoreable.get(
            ox_id=data["report_id"]
        )
        f = Framework.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["framework_id"]
        )

        sc = Scorecard.objects.create(
            report=r,
            framework=f,
            scorer=request.user,
            created_by=request.user,
            modified_by=request.user,
        )
        sc.save()
        # Add scores
        obj_list = []
        if "blank" in data and data["blank"] is True:
            for c in f.criteria:
                scs, _ = ScorecardScore.objects.get_or_create(
                    scorecard=sc,
                    criteria=c,
                )
                scs.created_by = request.user
                scs.modified_by = request.user
                scs.save()

        for s in data["scores"]:
            c = Criteria.objects.get(ox_id=s["criteria_id"], framework=f)
            scs, _ = ScorecardScore.objects.get_or_create(
                scorecard=sc,
                criteria=c,
            )
            scs.score = s.get("score", None)
            scs.comment = s.get("comment", None)
            scs.gpt_scored_last = s.get("gpt_scored_last", None)
            scs.created_by = request.user
            scs.modified_by = request.user
            scs.save()

        obj_list.extend([sc, r, f])

        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": sc,
        }


class UpdateScorecardHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # {
        #     "id": 514,
        #     "scores": [
        #         {
        # Existing
        #             "id": 123
        #             "comment": "Foo bar",
        #             "score": 5,
        #         },
        #         {
        # New
        #             "criteria_id": 22,
        #             "comment": "Ack",
        #             "score": 2,
        #         },
        #     ]
        # }

        sc = Scorecard.objects.get(ox_id=data["id"])
        # Ensure authorized.
        f = Framework.authorized_objects.authorize(user=request.user).findable.get(
            pk=sc.framework.pk
        )
        r = Report.authorized_objects.authorize(user=request.user).scoreable.get(
            pk=sc.report.pk
        )
        obj_list = [sc, r, f]
        for s in data["scores"]:
            if "id" in s:
                # We have an existing score we're updating.
                scs = ScorecardScore.objects.get(ox_id=s["id"], scorecard=sc)
                scs.modified_by = request.user
                c = scs.criteria
            else:
                c = Criteria.objects.get(ox_id=s["criteria_id"], framework=f)
                scs = ScorecardScore.objects.create(
                    scorecard=sc,
                    criteria=c,
                )
                scs.created_by = request.user
                scs.modified_by = request.user
                scs.save()

            scs.score = s.get("score", None)
            scs.gpt_scored_last = s.get("gpt_scored_last", None)
            scs.comment = s.get("comment", None)
            scs.save()
        sc.modified_by = request.user
        sc.save()
        sc = Scorecard.objects.get(pk=sc.pk)
        f = Framework.objects.get(pk=f.pk)
        r = Report.objects.get(pk=r.pk)

        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": sc,
        }


class DeleteScorecardHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        sc = Scorecard.objects.get(ox_id=data["id"])
        # Ensure authorized.
        f = Framework.authorized_objects.authorize(user=request.user).findable.get(
            pk=sc.framework.pk
        )
        r = Report.authorized_objects.authorize(user=request.user).scoreable.get(
            pk=sc.report.pk
        )
        assert f.pk is not None
        assert r.pk is not None
        assert r.can_write(user=request.user) or sc.scorer == request.user

        sc.delete()
        f = Framework.objects.get(pk=f.pk)
        r = Report.objects.get(pk=r.pk)
        # found = False
        # for sc in r.scorecards:
        #     if sc.framework == f:
        #         found = True

        return {
            "obj_list": [r, f],
            "success": True,
            "target_obj": None,
            "deleted": [
                {"type": "scorecards", "pk": data["id"]},
            ],
        }
