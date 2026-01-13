from api.events.base import BaseEventHandler
from frameworks.models import Framework, Criteria
from organizations.models import Organization, Team, User, GenericPermission
from collaboration.models import ObjectSubscription, InboxItem
from reports.models import Report
from sources.models import Source
from stacks.models import Stack
from django.contrib.contenttypes.models import ContentType


class UpdatePermissionsHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        if data["type"] == "report":
            obj = Report.authorized_objects.authorize(
                user=request.user
            ).administered.get(ox_id=data["id"])
        elif data["type"] == "framework":
            obj = Framework.authorized_objects.authorize(
                user=request.user
            ).administered.get(ox_id=data["id"])
        elif data["type"] == "source":
            obj = Source.authorized_objects.authorize(
                user=request.user
            ).administered.get(ox_id=data["id"])
        elif data["type"] == "stack":
            obj = Stack.authorized_objects.authorize(
                user=request.user
            ).administered.get(ox_id=data["id"])

        created_gps = []
        ret_list = []

        found_admin = False
        for perm in data["permissions"]:
            if perm.get("administer", False):
                found_admin = True
                break
        assert found_admin

        # One round making sure to set admin permissions
        for perm in data["permissions"]:
            if "administer" in perm and perm["administer"]:
                can_administer = "administer" in perm and perm.get("administer", False)
                can_write = "write" in perm and perm.get("write", False)
                permissions_kwargs = {
                    "acting_user": request.user,
                    "can_score": (
                        ("score" in perm and perm.get("score", False))
                        or can_write
                        or can_administer
                    ),
                    "can_read": (
                        ("read" in perm and perm.get("read", False))
                        or can_write
                        or can_administer
                    ),
                    "can_write": (can_write or can_administer),
                    "can_administer": can_administer,
                }

                if perm["type"] == "user":
                    role = User.objects.get(ox_id=perm["id"])
                    permissions_kwargs["user"] = role
                    ret_list.append(role)
                elif perm["type"] == "team":
                    role = Team.objects.get(ox_id=perm["id"])
                    permissions_kwargs["team"] = role
                    ret_list.append(role)
                elif perm["type"] == "organization":
                    role = Organization.objects.get(ox_id=perm["id"])
                    permissions_kwargs["organization"] = role
                    ret_list.append(role)

                created_gp = obj.set_permission(**permissions_kwargs)
                created_gps.append(created_gp.pk)

        # One round setting all the other permissions
        for perm in data["permissions"]:
            if "administer" not in perm or not perm["administer"]:
                can_administer = "administer" in perm and perm.get("administer", False)
                can_write = "write" in perm and perm.get("write", False)
                permissions_kwargs = {
                    "acting_user": request.user,
                    "can_score": (
                        ("score" in perm and perm.get("score", False))
                        or can_write
                        or can_administer
                    ),
                    "can_read": (
                        ("read" in perm and perm.get("read", False))
                        or can_write
                        or can_administer
                    ),
                    "can_write": (can_write or can_administer),
                    "can_administer": can_administer,
                }

                if perm["type"] == "user":
                    role = User.objects.get(ox_id=perm["id"])
                    permissions_kwargs["user"] = role
                    ret_list.append(role)
                elif perm["type"] == "team":
                    role = Team.objects.get(ox_id=perm["id"])
                    permissions_kwargs["team"] = role
                    ret_list.append(role)
                elif perm["type"] == "organization":
                    role = Organization.objects.get(ox_id=perm["id"])
                    permissions_kwargs["organization"] = role
                    ret_list.append(role)

                created_gp = obj.set_permission(**permissions_kwargs)
                created_gps.append(created_gp.pk)

        users_to_update = []
        # Finally, cache invalidate all members
        for perm in data["permissions"]:
            if perm["type"] == "user":
                role = User.objects.get(ox_id=perm["id"])
            elif perm["type"] == "team":
                role = Team.objects.get(ox_id=perm["id"])
                for m in role.members:
                    users_to_update.append(m)
            elif perm["type"] == "organization":
                role = Organization.objects.get(ox_id=perm["id"])
                for m in role.members:
                    users_to_update.append(m)

        # Remove anyone who no longer has permissions.
        ct = ContentType.objects.get_for_model(obj)
        stale_gps = GenericPermission.objects.filter(
            content_type=ct,
            object_id=obj.pk,
        ).exclude(pk__in=created_gps)
        for gp in stale_gps:
            if gp.user:
                users_to_update.append(gp.user)

                # Remove subscriptions to this item
                ObjectSubscription.objects.filter(
                    user=gp.user, content_type=ct, object_id=obj.pk
                ).delete()
                # Remove inbox items for those subscriptions
                InboxItem.objects.filter(
                    user=gp.user, content_type=ct, object_id=obj.pk
                ).delete()

            if gp.team:
                for m in gp.team.members:
                    users_to_update.append(m)
            if gp.organization:
                for m in gp.organization.members:
                    users_to_update.append(m)
            gp.delete()
            ret_list.append(obj)
        ret_list = users_to_update

        return {
            "obj_list": ret_list,
            "success": True,
            "target_obj": obj,
        }
