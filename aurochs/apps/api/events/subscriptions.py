from django.contrib.contenttypes.models import ContentType
from api.events.base import BaseEventHandler
from collaboration.models import InboxItem, ObjectSubscription
from frameworks.models import Framework
from reports.models import Report
from sources.models import Source
from stacks.models import Stack
from organizations.models import Organization, Team, User


class SubscribeHandler(BaseEventHandler):
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
            ObjectSubscription.objects.get_or_create(
                object_id=obj.pk, content_type=ct, user=request.user
            )
            return {
                "obj_list": [obj, request.user],
                "success": True,
                "target_obj": obj,
            }

        return {
            "obj_list": [],
            "success": False,
            "target_obj": None,
        }


class UnsubscribeHandler(BaseEventHandler):
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
            try:
                os = ObjectSubscription.objects.filter(
                    object_id=obj.pk, content_type=ct, user=request.user
                )
                os.delete()
            except ObjectSubscription.DoesNotExist:
                pass

            return {
                "obj_list": [obj, request.user],
                "success": True,
                "target_obj": obj,
            }

        return {
            "obj_list": [],
            "success": False,
            "target_obj": None,
        }


class MarkInboxItemDoneHandler(BaseEventHandler):
    def handle_event(self, request, data):
        ii = InboxItem.objects.get(ox_id=data["id"], user=request.user)
        ii.done = True
        ii.read = True
        ii.save()

        return {
            "obj_list": [ii, request.user],
            "success": True,
            "target_obj": ii,
        }


class MarkInboxItemActiveHandler(BaseEventHandler):
    def handle_event(self, request, data):
        ii = InboxItem.objects.get(ox_id=data["id"], user=request.user)
        ii.done = False
        ii.save()

        return {
            "obj_list": [ii, request.user],
            "success": True,
            "target_obj": ii,
        }


class MarkInboxItemReadHandler(BaseEventHandler):
    def handle_event(self, request, data):
        ii = InboxItem.objects.get(ox_id=data["id"], user=request.user)
        ii.read = True
        ii.save()

        return {
            "obj_list": [ii, request.user],
            "success": True,
            "target_obj": ii,
        }


class MarkInboxItemUnreadHandler(BaseEventHandler):
    def handle_event(self, request, data):
        ii = InboxItem.objects.get(ox_id=data["id"], user=request.user)
        ii.read = False
        ii.save()

        return {
            "obj_list": [ii, request.user],
            "success": True,
            "target_obj": ii,
        }
