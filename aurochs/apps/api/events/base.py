from django.conf import settings
import hashlib
import json
from django.contrib.auth import authenticate, login
from organizations.models import Organization, Team, User, GenericPermission
from organizations.serializers import OmniSerializer
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from api.tasks import update_affected_users


class BaseEventHandler:
    direct_event = False

    def handle(self, request, data, offline=False, all_data=False, **kwargs):
        self.request = request
        self.process_tags = False
        self.tagged_obj = None
        self.do_not_minimize = False

        public_oxid = data.get("public_oxid")
        password = data.get("password")
        if request.user.is_anonymous and public_oxid and password:
            u = User.objects.get(ox_id=public_oxid)
            user = authenticate(u.username, password)
            if user is not None:
                login(request, user)
            else:
                raise Exception("Unknown user")

        try:
            if hasattr(self, "handle_event"):
                cleaned_data = data
                if request.user.is_anonymous:
                    self.user_channel_id = request.session.session_key
                else:
                    self.user_channel_id = request.user.ox_id

                if self.direct_event:
                    event_dict = self.handle_event(request, data)
                    event_dict["direct_event"] = True
                    return json.dumps(event_dict)

                if "event_type" in cleaned_data:
                    del data["event_type"]
                if "_server_timestamp" in cleaned_data:
                    del data["_server_timestamp"]
                self.permissions_kwargs = {"acting_user": request.user}

                self.tags = None
                if "tags" in data:
                    self.tags = data["tags"]
                    del data["tags"]

                event_dict = self.handle_event(request, data)
                # We were overridden by the handler.
                if self.direct_event:
                    event_dict["direct_event"] = True
                    return json.dumps(event_dict)
                update_dict = {"success": event_dict["success"]}
                if "data_override" in event_dict:
                    resp_dict = event_dict["data_override"]
                    resp_dict.update(update_dict)
                    return json.dumps(resp_dict)

                if self.process_tags:
                    active_tags, deleted_tags = self.handle_tags(self.tagged_obj)
                    update_dict["deleted"] = [
                        {"type": "tags", "pk": t} for t in deleted_tags
                    ]

                if "target_obj" in event_dict and event_dict["target_obj"]:
                    o = event_dict["target_obj"]
                    update_dict["target_obj_type"] = f"{o.__class__.__name__.lower()}"
                    update_dict["target_obj_id"] = f"{o.pk}"
                    update_dict["target_obj_ox_id"] = f"{o.ox_id}"
                    update_dict[
                        "target_obj"
                    ] = f"window.aurochs.data.{o.__class__.__name__.lower()}['{o.ox_id}']"
                    update_dict["obj_pk"] = o.ox_id

                serializer = OmniSerializer(request.user)
                js_data = serializer.serialize_to_js_lines()

                last_lines = []
                if not all_data:
                    last_lines = request.user.cached_data_lines().split("\n")

                obj_pairs = []

                for l in js_data.split("\n"):
                    if self.do_not_minimize or l not in last_lines:
                        pair = l.split(" = ")
                        # If the line is new or changed, include it.
                        obj_pairs.append(
                            [
                                pair[0],
                                pair[1],
                            ]
                        )

                resp_dict = {}
                request.user.save_data_lines_to_cache(js_data)

                if "deleted" in event_dict:
                    resp_dict["deleted"] = event_dict["deleted"]
                if "_server_timestamp" in data:
                    update_dict["_server_timestamp"] = data["_server_timestamp"]
                resp_dict.update(update_dict)

                # Dump to serialized format.
                ret_source = json.dumps(resp_dict)
                ret = ret_source[:-1] + ', "objs": ['
                for pair in obj_pairs:
                    val = pair[1]
                    key = pair[0].replace('"', "'")
                    if val[-1:] == ";":
                        val = val[:-1]
                    d = {}
                    d[key] = val
                    ret += json.dumps(d) + ", "
                if len(obj_pairs) > 0:
                    ret = ret[:-2]
                ret += "]" + ret_source[-1:]

                if not offline:
                    # Update all other connected users.
                    if "target_obj_type" in update_dict:
                        update_affected_users.delay(
                            update_dict["target_obj_type"],
                            update_dict["target_obj_id"],
                            self.request.user.pk,
                        )

                    for o in event_dict["obj_list"]:
                        target_obj_type = f"{o.__class__.__name__.lower()}"
                        target_obj_id = f"{o.pk}"

                        update_affected_users.delay(
                            target_obj_type,
                            target_obj_id,
                            self.request.user.pk,
                        )

                return ret
        except:
            if settings.DEBUG or settings.TEST_MODE:
                import traceback

                traceback.print_exc()
                pass
            if (
                not settings.AIRGAPPED
                and not settings.DEBUG
                and not settings.TEST_MODE
                and not settings.DEV_MODE
            ):
                import sentry_sdk

                sentry_sdk.capture_exception()
            return json.dumps({"success": False, "error_message": "Server error."})
        return json.dumps({"success": False, "error_message": "Missing event handler."})

    def return_object_pairs(self, lines, shallow=False):
        pair_lines = []
        for l in lines:
            obj = l[: l.find(" = ")]
            val = l[l.find(" = ") + 3 : -1]
            if obj and val and obj != "" and val != "":
                d = {}
                d[obj] = val
                pair_lines.append(d)
        return pair_lines

    def handle_pseudoteam(self, data):
        self.specified_permissions = False
        if "pseudoteam" in data:
            try:
                team_type, team_id = data["pseudoteam"].split("__")
                if team_type == "team":
                    team = Team.objects.get(pk=team_id)
                    self.specified_permissions = True
                    self.permissions_kwargs.update(
                        {
                            "team": team,
                            "can_score": True,
                            "can_read": True,
                            "can_write": True,
                            "can_administer": True,
                        }
                    )
                elif team_type == "user":
                    user = User.objects.get(pk=team_id)
                    self.specified_permissions = True
                    self.permissions_kwargs.update(
                        {
                            "user": user,
                            "can_score": True,
                            "can_read": True,
                            "can_write": True,
                            "can_administer": True,
                        }
                    )
                elif team_type == "organization":
                    organization = Organization.objects.get(pk=team_id)
                    self.specified_permissions = True
                    self.permissions_kwargs.update(
                        {
                            "organization": organization,
                            "can_score": True,
                            "can_read": True,
                            "can_write": True,
                            "can_administer": True,
                        }
                    )
                if self.specified_permissions:
                    self.team_type = team_type

            except:
                import traceback

                # traceback.print_exc()
                pass

    def add_pseudoteam_permissions(self, obj, request, created=False):
        # TODO: Remove this once we have proper permissions.
        # Scorched earth one ring to rule them all kind of solution, super non-ideal.
        if self.specified_permissions or created:
            if self.specified_permissions:
                gp = obj.set_permission(**self.permissions_kwargs)
            elif created:
                gp = obj.set_permission(
                    acting_user=request.user,
                    user=request.user,
                    can_score=True,
                    can_read=True,
                    can_write=True,
                    can_administer=True,
                )

            ct = ContentType.objects.get_for_model(obj)
            for g in GenericPermission.objects.filter(
                content_type=ct,
                object_id=obj.pk,
            ).all():
                if g.pk != gp.pk:
                    g.delete()

        # TODO: Future, delete all of the above, and just uncomment this out.
        # if self.specified_permissions:
        #     obj.set_permission(**self.permissions_kwargs)
        # else:
        #     obj.set_permission(
        #         acting_user=request.user,
        #         user=request.user,
        #         can_score=True,
        #         can_read=True,
        #         can_write=True,
        #         can_administer=True,
        #     )

    def handle_tags(self, obj):
        active_tags = []
        deleted_tags = []
        # print("handle_tags")
        # print(self.tags)
        if self.tags is not None:
            active_tags, deleted_tags = obj.set_tags(self.tags, self.request.user)
        return active_tags, deleted_tags
