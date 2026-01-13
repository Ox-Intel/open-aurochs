from api.events.base import BaseEventHandler
from reports.models import Report, Scorecard
from collaboration.models import ObjectSubscription
from frameworks.models import Framework
from sources.models import Source
from stacks.models import Stack
from organizations.models import GenericPermission
from django.contrib.contenttypes.models import ContentType


class CreateReportHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.

        self.process_tags = True
        self.handle_pseudoteam(data)
        if self.specified_permissions:
            del data["pseudoteam"]

        s = None
        if "source_id" in data:
            source_id = data["source_id"]
            del data["source_id"]
            s = Source.authorized_objects.authorize(user=request.user).get(
                ox_id=source_id
            )

        r = Report.authorized_objects.authorize(user=request.user).create(**data)

        self.add_pseudoteam_permissions(r, request, created=True)
        r.save()
        ret_list = []
        if s:
            r.sources.add(s)
            r.save()

            s = Source.objects.get(pk=s.pk)
            ret_list.append(s)

        # Subscribe the creator to this object.
        ct = ContentType.objects.get_for_model(r)
        ObjectSubscription.objects.get_or_create(
            object_id=r.pk, content_type=ct, user=request.user
        )

        ret_list.append(r)
        self.tagged_obj = r

        return {
            "obj_list": ret_list,
            "success": True,
            "target_obj": r,
        }


class UpdateReportHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.process_tags = True
        self.handle_pseudoteam(data)
        if self.specified_permissions:
            del data["pseudoteam"]
        r = Report.authorized_objects.authorize(user=request.user).writeable.get(
            ox_id=data["id"]
        )

        updated_report = False
        for k, v in data.items():
            if k in Report.api_writable_fields:
                if getattr(r, k) != v:
                    setattr(r, k, v)
                    updated_report = True

        if updated_report:
            r.modified_by = request.user
            r.save()
        # TODO when we want history changes, uncomment this.
        # r.generate_history_change(request.user, "update_report")
        self.add_pseudoteam_permissions(r, request)
        r = Report.objects.get(pk=r.pk)
        obj_list = [
            r,
        ]
        self.tagged_obj = r
        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": r,
            "shallow": not updated_report,
        }


class DeleteReportHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        r = Report.authorized_objects.authorize(user=request.user).administered.get(
            ox_id=data["id"]
        )
        self.process_tags = False
        if "tags" in data:
            del data["tags"]
        self.tags = []
        self.handle_tags(r)

        related_stacks = [
            s for s in Stack.objects.filter(reports=r).values_list("pk", flat=True)
        ]
        Scorecard.objects.filter(report=r).delete()

        r.delete()
        self.tags = None

        obj_list = []

        all_related_stacks = Stack.objects.filter(pk__in=related_stacks)
        for s in all_related_stacks:
            s.reports.remove(r)

        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": None,
            "deleted": [
                {"type": "reports", "pk": data["id"]},
            ],
        }


class GetReportHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.cacheable_event = True
        r = Report.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["id"]
        )
        return {
            "obj_list": [
                r,
            ],
            "success": True,
            "target_obj": r,
        }


class GetReportsHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        r = Report.authorized_objects.authorize(user=request.user).findable.filter(
            **data
        )
        return {
            "obj_list": r.all(),
            "success": True,
            "target_obj": None,
        }


class AddSourceToReportHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        r = Report.authorized_objects.authorize(user=request.user).scoreable.get(
            ox_id=data["report_id"]
        )
        s = Source.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["source_id"]
        )
        r.sources.add(s)
        r.updated_by = request.user
        r.save()

        return {
            "obj_list": [
                r,
                s,
            ],
            "success": True,
            "target_obj": r,
        }


class RemoveSourceFromReportHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        r = Report.authorized_objects.authorize(user=request.user).scoreable.get(
            ox_id=data["report_id"]
        )
        s = Source.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["source_id"]
        )
        r.sources.remove(s)
        r.updated_by = request.user
        r.save()

        return {
            "obj_list": [
                r,
                s,
            ],
            "success": True,
            "target_obj": r,
        }
