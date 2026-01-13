from api.events.base import BaseEventHandler
from frameworks.models import Framework, Criteria
from organizations.models import (
    GenericPermission,
    Team,
    TeamMember,
    Organization,
    OrganizationRole,
    User,
)
from collaboration.models import ObjectSubscription, InboxItem
from reports.models import Report
from django.contrib.contenttypes.models import ContentType


class CreateOrganizationHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.

        if "blank" in data and data["blank"] is True:
            del data["blank"]
            if "name" not in data:
                data["name"] = "New Organization"
        o = Organization.objects.create(**data)
        o.created_by = request.user
        o.modified_by = request.user
        o.save()
        o.add_user(request.user, can_view=True, can_manage=True)

        obj_list = [
            o,
        ]

        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": o,
        }


class UpdateOrganizationHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        ret_list = []
        created_org_roles = []
        o = Organization.objects.get(ox_id=data["id"])
        assert o.can_manage(request.user)
        updated_organization = False

        for k, v in data.items():
            if k in Organization.api_writable_fields:
                if getattr(o, k) != v:
                    setattr(o, k, v)
                    updated_organization = True

        if updated_organization:
            o.modified_by = request.user
            o.save()

        if "members" in data:
            found_manager = False
            for member in data["members"]:
                if member["can_manage"]:
                    found_manager = True
                    break

            assert found_manager

            for member in data["members"]:
                u = User.objects.get(ox_id=member["id"])
                org_role, created = OrganizationRole.objects.get_or_create(
                    organization=o, user=u
                )
                org_role.can_view = member["can_view"]
                org_role.can_manage = member["can_manage"]
                org_role.save()

                ret_list.append(u)
                updated_organization = True

                created_org_roles.append(org_role.pk)

            # Handle users who were removed from the org.
            removed_users = []
            for org_role in (
                OrganizationRole.objects.filter(organization=o)
                .exclude(pk__in=created_org_roles)
                .all()
            ):
                removed_user = org_role.user
                for tm in TeamMember.objects.filter(
                    team__organization=o, user=removed_user
                ).all():
                    tm.delete()

                removed_users.append(removed_user)
                org_role.delete()

            # Separate loop to reduce the queries
            for org_gp in GenericPermission.objects.filter(organization=o).all():
                for removed_user in removed_users:
                    if (
                        GenericPermission.objects.filter(
                            content_type=org_gp.content_type,
                            object_id=org_gp.object_id,
                            user=removed_user,
                        ).count()
                        == 0
                    ):
                        # Remove subscriptions to this item
                        ObjectSubscription.objects.filter(
                            user=removed_user,
                            content_type=org_gp.content_type,
                            object_id=org_gp.object_id,
                        ).all().delete()
                        # Remove inbox items for those subscriptions
                        InboxItem.objects.filter(
                            user=removed_user,
                            content_type=org_gp.content_type,
                            object_id=org_gp.object_id,
                        ).all().delete()

                    ret_list.append(removed_user)

        o = Organization.objects.get(pk=o.pk)
        ret_list.append(o)

        return {
            "obj_list": ret_list,
            "shallow": not updated_organization,
            "success": True,
            "target_obj": o,
        }


class DeleteOrganizationHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        o = Organization.objects.get(ox_id=data["id"])
        assert o.can_manage(request.user) and o.can_be_deleted

        o.delete()

        return {
            "obj_list": [],
            "success": True,
            "target_obj": None,
            "deleted": [
                {"type": "organizations", "pk": data["id"]},
            ],
        }


class GetOrganizationHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.cacheable_event = True
        o = Organization.objects.get(ox_id=data["id"])
        assert o.can_view(request.user) or o.can_manage(request.user)

        return {
            "obj_list": [
                o,
            ],
            "success": True,
            "target_obj": o,
        }
