from api.events.base import BaseEventHandler
from collaboration.models import ObjectSubscription
from stacks.models import Stack
from reports.models import Report
from organizations.models import Organization, Team, User
from django.contrib.contenttypes.models import ContentType


class CreateStackHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # Handle old client code
        # TODO #VUEMIGRATION remove this when we migrate to vue.
        self.process_tags = True
        self.handle_pseudoteam(data)
        if self.specified_permissions:
            del data["pseudoteam"]
        obj = Stack.authorized_objects.authorize(user=request.user).create(**data)
        obj.created_by = request.user
        obj.modified_by = request.user
        self.add_pseudoteam_permissions(obj, request, created=True)
        obj.save()

        obj_list = [
            obj,
        ]
        self.tagged_obj = obj

        # Subscribe the creator to this object.
        ct = ContentType.objects.get_for_model(obj)
        ObjectSubscription.objects.get_or_create(
            object_id=obj.pk, content_type=ct, user=request.user
        )

        # Required so we invalidate and update permissions.

        obj_list.append(request.user)
        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": obj,
        }


class UpdateStackHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.process_tags = True
        self.handle_pseudoteam(data)
        if self.specified_permissions:
            del data["pseudoteam"]
        obj = Stack.authorized_objects.authorize(user=request.user).writeable.get(
            ox_id=data["id"]
        )
        updated_stack = False
        for k, v in data.items():
            if k in Stack.api_writable_fields:
                if getattr(obj, k) != v:
                    setattr(obj, k, v)
                    updated_stack = True
        if updated_stack:
            obj.modified_by = request.user
            obj.save()
        # TODO when we want history changes, uncomment this.
        # obj.generate_history_change(request.user, "update_stack")
        self.add_pseudoteam_permissions(obj, request)

        obj = Stack.objects.get(pk=obj.pk)
        obj_list = [
            obj,
        ]
        self.tagged_obj = obj
        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": obj,
            "shallow": not updated_stack,
        }


class DeleteStackHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # Clear all tags off the object before deleting.
        self.process_tags = False
        if "tags" in data:
            del data["tags"]
        self.tags = []
        obj = Stack.authorized_objects.authorize(user=request.user).administered.get(
            ox_id=data["id"]
        )
        self.handle_tags(obj)

        related_reports = [r for r in obj.reports.values_list("pk", flat=True)]
        obj.delete()
        self.tags = None

        reports = []
        all_related = Report.authorized_objects.authorize(
            user=request.user
        ).findable.filter(pk__in=related_reports)
        for r in all_related:
            reports.append(r)

        return {
            "obj_list": reports,
            "success": True,
            "target_obj": None,
            "deleted": [
                {"type": "stacks", "pk": data["id"]},
            ],
        }


class GetStackHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.cacheable_event = True
        s = Stack.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["id"]
        )
        return {
            "obj_list": [
                s,
            ],
            "success": True,
            "target_obj": s,
        }


class GetStacksHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.cacheable_event = True
        s = Stack.authorized_objects.authorize(user=request.user).findable.filter(
            **data
        )
        return {
            "obj_list": s.all(),
            "success": True,
            "target_obj": None,
        }


class AddReportToStackHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        r = Report.authorized_objects.authorize(user=request.user).scoreable.get(
            ox_id=data["report_id"]
        )
        s = Stack.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["stack_id"]
        )
        s.reports.add(r)
        s.updated_by = request.user
        s.save()

        return {
            "obj_list": [
                r,
                s,
            ],
            "success": True,
            "target_obj": s,
        }


class RemoveReportFromStackHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        r = Report.authorized_objects.authorize(user=request.user).scoreable.get(
            ox_id=data["report_id"]
        )
        s = Stack.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["stack_id"]
        )
        s.reports.remove(r)
        s.updated_by = request.user
        s.save()

        return {
            "obj_list": [
                r,
                s,
            ],
            "success": True,
            "target_obj": s,
        }
