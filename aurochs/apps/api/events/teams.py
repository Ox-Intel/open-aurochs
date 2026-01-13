from api.events.base import BaseEventHandler
from frameworks.models import Framework, Criteria
from organizations.models import GenericPermission, Team, TeamMember, Organization, User
from django.contrib.contenttypes.models import ContentType


class CreateTeamHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.

        if "blank" in data and data["blank"] is True:
            if "name" not in data:
                data["name"] = "New Team"
        org = Organization.objects.get(ox_id=data["org_id"])
        assert org.can_manage(request.user) or org.can_view(request.user)

        t = Team.objects.create(name=data["name"], organization=org)
        if "description" in data:
            t.description = data["description"]
        t.created_by = request.user
        t.modified_by = request.user
        t.save()
        t.add_user(request.user, can_view=True, can_manage=True)

        obj_list = [
            t,
        ]

        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": t,
        }


class UpdateTeamHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        ret_list = []
        created_tms = []
        t = Team.objects.get(ox_id=data["id"])
        assert t.can_manage(request.user) or t.organization.can_manage(request.user)
        updated_team = False

        for k, v in data.items():
            if k in Team.api_writable_fields:
                if getattr(t, k) != v:
                    setattr(t, k, v)
                    updated_team = True
        if updated_team:
            t.modified_by = request.user
            t.save()

        if "members" in data:
            for member in data["members"]:
                u = User.objects.get(ox_id=member["id"])
                tm, created = TeamMember.objects.get_or_create(team=t, user=u)
                tm.can_view = member["can_view"]
                tm.can_manage = member["can_manage"]
                tm.save()
                updated_team = True

                ret_list.append(u)

                created_tms.append(tm.pk)

            if len(created_tms) == 0:
                TeamMember.objects.filter(team=t).delete()
            else:
                TeamMember.objects.filter(team=t).exclude(pk__in=created_tms).delete()

        ret_list.append(t)

        o = t.organization
        ret_list.append(o)

        return {
            "obj_list": ret_list,
            "shallow": not updated_team,
            "success": True,
            "target_obj": t,
        }


class DeleteTeamHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        t = Team.objects.get(ox_id=data["id"])
        assert (
            t.can_manage(request.user) or t.organization.can_manage(request.user)
        ) and t.can_be_deleted

        t.delete()

        return {
            "obj_list": [],
            "success": True,
            "target_obj": None,
            "deleted": [
                {"type": "teams", "pk": data["id"]},
            ],
        }


class GetTeamHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.cacheable_event = True
        t = Team.objects.get(ox_id=data["id"])
        assert (
            t.can_view(request.user)
            or t.can_manage(request.user)
            or t.organization.can_manage(request.user)
        )

        return {
            "obj_list": [
                t,
            ],
            "success": True,
            "target_obj": t,
        }
