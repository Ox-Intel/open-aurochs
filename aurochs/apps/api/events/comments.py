from django.contrib.contenttypes.models import ContentType
from api.events.base import BaseEventHandler
from collaboration.models import ObjectSubscription, Comment
from frameworks.models import Framework
from reports.models import Report
from sources.models import Source
from stacks.models import Stack
from organizations.models import Organization, Team, User
from collaboration.models import InboxItem


class AddCommentHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        obj = False
        if "object_type" in data and "id" in data:
            if data["object_type"] == "framework":
                obj = Framework.authorized_objects.authorize(
                    user=request.user
                ).findable.get(ox_id=data["id"])
            elif data["object_type"] == "report":
                obj = Report.authorized_objects.authorize(
                    user=request.user
                ).findable.get(ox_id=data["id"])
            elif data["object_type"] == "source":
                obj = Source.authorized_objects.authorize(
                    user=request.user
                ).findable.get(ox_id=data["id"])
            elif data["object_type"] == "stack":
                obj = Stack.authorized_objects.authorize(
                    user=request.user
                ).findable.get(ox_id=data["id"])

        if obj:
            ct = ContentType.objects.get_for_model(obj)
            c = Comment.objects.create(
                object_id=obj.pk,
                content_type=ct,
                user=request.user,
                body=data["body"],
                created_by=request.user,
            )
            obj_list = [c, obj]

            return {
                "obj_list": obj_list,
                "success": True,
                "target_obj": c,
            }

        return {
            "obj_list": [],
            "success": False,
            "target_obj": None,
        }


class UpdateCommentHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        c = Comment.objects.get(ox_id=data["id"], user=request.user)
        c.body = data["body"]
        c.edited = True
        c.save()

        obj_list = [c, c.content_object]

        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": c,
        }


class DeleteCommentHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        c = Comment.objects.get(ox_id=data["id"], user=request.user)
        obj = c.content_object
        c.delete()

        return {
            "obj_list": [
                obj,
            ],
            "success": True,
            "target_obj": obj,
        }
