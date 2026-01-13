import logging
from api.events.base import BaseEventHandler
from sources.models import Source
from organizations.models import Organization, Team, User
from collaboration.models import InboxItem
from stacks.models import Stack
from frameworks.models import Framework
from reports.models import Report


class ChangePasswordHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        if "new_password" in data:
            u = request.user
            u.set_password(data["new_password"])
            u.save()
        return {
            "obj_list": [],
            "success": True,
            "target_obj": u,
        }


class UpdateMyUserHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        updateable_fields = [
            "first_name",
            "last_name",
            "email",
            "username",
        ]
        u = request.user
        changed = False
        for f in updateable_fields:
            if f in data:
                if data[f] != getattr(u, f):
                    setattr(u, f, data[f])
                    changed = True
        if changed:
            u.save()

        return {
            "obj_list": [
                u,
            ],
            "success": True,
            "target_obj": u,
        }


class CreateUserHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        o = Organization.objects.get(ox_id=data["org_id"])
        assert o.can_manage(request.user)

        u = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            username=data["username"],
        )
        u.set_password(data["password"])
        u.is_active = True
        u.save()

        o.add_user(u, can_view=True, can_manage=False)

        return {
            "obj_list": [
                u,
                o,
            ],
            "success": True,
            "target_obj": u,
        }


class GetMyUserHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # self.cacheable_event = True
        self.do_not_minimize = True
        u = request.user
        objs = [
            u,
        ]
        # objs.extend(u.inbox_items)

        # for ii in u.inbox_items:
        #     if ii.comment:
        #         objs.append(ii.comment)
        #         objs.append(ii.initiator)
        return {
            "obj_list": objs,
            "success": True,
            "target_obj": u,
        }


class CheckAvailableUsername(BaseEventHandler):
    def handle_event(self, request, data):
        self.cacheable_event = False
        found_user = True
        if "username" in data:
            found_user = User.objects.filter(username=data.get("username")).count() > 0

        return {
            "data_override": {"available": not found_user},
            "success": True,
        }


class UpdateMyPinsHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        updateable_fields = [
            "pinned_stack",
            "pinned_report",
            "pinned_framework",
        ]
        u = request.user
        # changed = False
        for f in updateable_fields:
            if f in data:
                if f.split("_")[-1] == "stack":
                    obj = Stack.authorized_objects.authorize(user=request.user).get(
                        ox_id=data[f]
                    )
                elif f.split("_")[-1] == "report":
                    obj = Report.authorized_objects.authorize(user=request.user).get(
                        ox_id=data[f]
                    )
                elif f.split("_")[-1] == "framework":
                    obj = Framework.authorized_objects.authorize(user=request.user).get(
                        ox_id=data[f]
                    )
                if "unpin" in data and data["unpin"]:
                    setattr(u, f, None)
                    # changed = True
                else:
                    # if obj != getattr(u, f):
                    setattr(u, f, obj)
                    # changed = True
        # if changed:
        u.save()

        return {
            "obj_list": [
                u,
            ],
            "success": True,
            "target_obj": u,
        }
