import json
from datetime import datetime
from decimal import Decimal

from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from utils.helpers import OBJ_ORDERS, _obj_key


from frameworks.models import Criteria, Framework
from organizations.models import (
    Organization,
    Team,
    TeamMember,
    User,
    OrganizationRole,
    Tag,
    TaggedObject,
    GenericPermission,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback
from stacks.models import Stack
from collaboration.models import ObjectSubscription, Comment, InboxItem
from history.models import ObjectHistoryChange

REL_SPLIT_START = "__MAGIC_REL_SPLIT_START__"
REL_SPLIT_END = "__MAGIC_REL_SPLIT_END__"


class SerializationHelpers(object):
    def datetime_ms(self, dt):
        if dt:
            return dt.timestamp() * 1000
        return None

    def rel_by_id(self, class_name, obj_pk):
        if obj_pk:
            return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{obj_pk}']{REL_SPLIT_END}"
        return None

    def get_ox_id_from_user_id(self, user_id):
        return self.get_ox_id_from_object_id("users", user_id)

    def get_ox_id_from_object_id(self, object_type, object_id):
        try:
            return self.object_ids_to_ox_id[object_type][str(object_id)]
        except:
            print("falling back")
            print(object_type)
            print(object_id)
            if object_id:
                return (
                    getattr(self, f"all_{object_type}", {})
                    .get(str(object_id), {})
                    .get("ox_id", None)
                )
            return None

    def get_gp_count(
        self,
        target_gps,
        permission_type,
        permission_id,
    ):
        matches = {}
        for gp in target_gps:
            if (
                f"{permission_type}_id" in gp
                and gp[f"{permission_type}_id"] == permission_id
            ):
                matches[str(gp["object_id"])] = True

        return len(matches.keys())

    def last_admin_for_count(self, permission_type, permission_id):
        num_last_admin = 0
        if str(permission_id) in self.gps_by_holders[permission_type]:
            for team_obj_gp in self.gps_by_holders[permission_type][str(permission_id)]:
                # All of the objects this team has some permissions to.
                team_has_admin = False
                other_admins_exist = False
                for gp in self.gps_by_ct_id[str(team_obj_gp["content_type_id"])][
                    str(team_obj_gp["object_id"])
                ]:
                    if (
                        permission_type == "team"
                        and gp["team_id"] == permission_id
                        and gp["can_administer"]
                    ):
                        team_has_admin = True
                    if (
                        permission_type == "organization"
                        and gp["organization_id"] == permission_id
                        and gp["can_administer"]
                    ):
                        team_has_admin = True
                    elif gp["can_administer"]:
                        other_admins_exist = True
                if team_has_admin and not other_admins_exist:
                    num_last_admin += 1
        return num_last_admin

    def get_comments(self, content_type, id):
        if str(self.content_types[content_type]) in self.all_comments_by_ct_and_id and (
            str(id)
            in self.all_comments_by_ct_and_id[str(self.content_types[content_type])]
        ):
            return self.all_comments_by_ct_and_id[
                str(self.content_types[content_type])
            ][str(id)]
        return []

    def get_tags(self, content_type, id):
        tos = []
        tags = []
        ct = str(self.content_types[content_type])
        id = str(id)
        if (
            ct in self.all_tagged_objs_by_ct_and_id
            and id in self.all_tagged_objs_by_ct_and_id[ct]
        ):
            tos = self.all_tagged_objs_by_ct_and_id[ct][id]
        for to in tos:
            tags.append(self.tags_by_id[str(to["tag_id"])])

        return tags

    def get_permissions(self, permission_type, permission_id):
        perms = {}
        if str(permission_id) in self.gps_by_objects[permission_type]:
            for team_obj_gp in self.gps_by_objects[permission_type][str(permission_id)]:
                # All of the objects this team has some permissions to.
                for gp in self.gps_by_ct_id[str(team_obj_gp["content_type_id"])][
                    str(team_obj_gp["object_id"])
                ]:
                    id_str = ""
                    if gp["team_id"]:
                        id_str = (
                            "T-%s"
                            % self.object_ids_to_ox_id["teams"][str(gp["team_id"])]
                        )
                    elif gp["user_id"]:
                        if str(gp["user_id"]) in self.object_ids_to_ox_id["users"]:
                            id_str = (
                                "U-%s"
                                % self.object_ids_to_ox_id["users"][str(gp["user_id"])]
                            )
                    elif gp["organization_id"]:
                        if (
                            str(gp["organization_id"])
                            in self.object_ids_to_ox_id["organizations"]
                        ):
                            id_str = (
                                "O-%s"
                                % self.object_ids_to_ox_id["organizations"][
                                    str(gp["organization_id"])
                                ]
                            )

                    if id_str:
                        perm_str = ""
                        if gp["can_score"]:
                            perm_str += "1"
                        else:
                            perm_str += "0"
                        if gp["can_read"]:
                            perm_str += "1"
                        else:
                            perm_str += "0"
                        if gp["can_write"]:
                            perm_str += "1"
                        else:
                            perm_str += "0"
                        if gp["can_administer"]:
                            perm_str += "1"
                        else:
                            perm_str += "0"
                        perms[id_str] = perm_str
        return perms

    def is_subscribed(self, content_type, id):
        return (
            str(self.content_types[content_type])
            in self.object_subscriptions_by_ct_and_id
            and str(id)
            in self.object_subscriptions_by_ct_and_id[
                str(self.content_types[content_type])
            ]
        )

    def all_subscribers(self, content_type, id):
        subscribers = []
        ct = str(self.content_types[content_type])
        id = str(id)
        if (
            ct in self.all_object_subscriptions_by_ct_and_id
            and id in self.all_object_subscriptions_by_ct_and_id[ct]
        ):
            for sub in self.all_object_subscriptions_by_ct_and_id[ct][id]:
                subscribers.append(sub)
        return subscribers

    def get_search_text(self, obj_type, obj, tags=[]):
        ox_id = obj["ox_id"]
        text = f"{obj_type}:{ox_id}"
        if obj["name"]:
            text += "|name:" + obj["name"]

        tags = self.get_tags(obj_type, obj["id"])

        for t in tags:
            if t["name"]:
                text += "|tag:" + t["name"]

        if obj_type == "report":
            for s in self.all_related_to_object_in_field_list(
                self.all_stacks, "report_ids", obj["id"]
            ):
                if s["name"]:
                    text += "|instk:" + s["name"]

        if text != "":
            return text + "|"
        return text

    def all_related_to_object_in_field_list(self, obj_list, field, target_id):
        found_list = []
        for obj in obj_list:
            if target_id in obj[field]:
                found_list.append(obj)
        return found_list


class OmniSerializer(SerializationHelpers):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.user_data_to_serialize = {}
        self.serialized_objects = {}
        self.all_user_data = {
            "users": {},
            "reports": {},
            "frameworks": {},
            "criteria": {},
            "sources": {},
            "stacks": {},
        }
        self.object_ids_to_ox_id = {
            "users": {},
            "teams": {},
            "organizations": {},
            "reports": {},
            "frameworks": {},
            "criterias": {},
            "sources": {},
            "stacks": {},
            "tags": {},
        }

    def serialize(self):
        self.get_content_types()
        self.fetch_all_user_data()
        self.create_user_dict()
        self.serialize_user_dict()
        # print(self.serialized_objects)
        return self.serialized_objects

    def serialize_to_json(self):
        ret = json.dumps(self.serialize(), sort_keys=True, cls=DjangoJSONEncoder)
        ret = ret.replace(f'"{REL_SPLIT_START}', "")
        ret = ret.replace(f'{REL_SPLIT_END}"', "")
        ret = ret.replace(f"{REL_SPLIT_START}", "")
        ret = ret.replace(f"{REL_SPLIT_END}", "")
        return ret

    def obj_to_json(self, obj):
        ret = json.dumps(obj, sort_keys=True, cls=DjangoJSONEncoder)
        ret = ret.replace(f'"{REL_SPLIT_START}', "")
        ret = ret.replace(f'{REL_SPLIT_END}"', "")
        ret = ret.replace(f"{REL_SPLIT_START}", "")
        ret = ret.replace(f"{REL_SPLIT_END}", "")
        return ret

    def serialize_to_js_lines(self):
        data = self.serialize()
        object_str = ""
        for obj_type, objects in data.items():
            for ox_id, obj in objects.items():
                object_str += (
                    f'window.aurochs.data.{obj_type}["{ox_id}"] = '
                    + self.obj_to_json(obj)
                    + "\n"
                )

        lines = object_str.split("\n")

        unique_lines = []
        object_keys = {}
        object_types = {}
        for l in lines:
            if l.startswith("window.aurochs.data."):
                object_type = l[len("window.aurochs.data.") : l.find("[")]
                object_key = l[: l.find(" = ")]
                if object_key not in object_keys:
                    unique_lines.append(l)
                object_types[object_type] = True
                object_keys[object_key] = True

        unique_lines = sorted(list(unique_lines), key=_obj_key)

        model_str = ""
        for o in object_types.keys():
            model_str += (
                f"window.aurochs.data.{o} = window.aurochs.data.{o} || " + "{};\n"
            )

        output_str = model_str + ";\n".join(unique_lines) + ";"
        output_str = output_str.replace("\n;\n", "\n").replace(";;", ";")
        return mark_safe(output_str)

    def get_content_types(self):
        cts = ContentType.objects.all().values("id", "app_label", "model")
        ct_framework_id = None
        ct_report_id = None
        ct_source_id = None
        ct_stack_id = None
        for ct in cts:
            if ct["model"] == "framework":
                ct_framework_id = ct["id"]
            if ct["model"] == "report":
                ct_report_id = ct["id"]
            if ct["model"] == "source":
                ct_source_id = ct["id"]
            if ct["model"] == "stack":
                ct_stack_id = ct["id"]
        self.content_types = {
            "framework": ct_framework_id,
            "report": ct_report_id,
            "source": ct_source_id,
            "stack": ct_stack_id,
        }
        self.content_types_by_id = {}
        self.content_types_by_id[str(ct_framework_id)] = "framework"
        self.content_types_by_id[str(ct_report_id)] = "report"
        self.content_types_by_id[str(ct_source_id)] = "source"
        self.content_types_by_id[str(ct_stack_id)] = "stack"

    def get_ox_id_from_user_id(self, user_id):
        return self.all_users_by_id.get(user_id, {}).get("ox_id", None)

    def add_to_serialized(self, obj_type, id, data):
        if obj_type not in self.serialized_objects:
            self.serialized_objects[obj_type] = {}
        self.serialized_objects[obj_type][id] = data

    def add_to_all_user_data(self, obj_type, id, data):
        if id:
            if obj_type not in self.all_user_data:
                self.all_user_data[obj_type] = {}
            self.all_user_data[obj_type][id] = data
        else:
            self.all_user_data[obj_type] = data

        if obj_type not in self.object_ids_to_ox_id:
            self.object_ids_to_ox_id[obj_type] = {}
        self.object_ids_to_ox_id[obj_type][str(data["id"])] = data["ox_id"]

    def serialize_from_dict(self, obj_type, o, **kwargs):
        ret = None
        if obj_type == "user" and o["ox_id"] == self.user.ox_id:
            ret = self.serialize_my_user(o, **kwargs)
        elif obj_type == "user":
            ret = self.serialize_user(o, **kwargs)
        elif obj_type == "team":
            ret = self.serialize_team(o, **kwargs)
        elif obj_type == "organization":
            ret = self.serialize_organization(o, **kwargs)
        elif obj_type == "stack":
            ret = self.serialize_stack(o, **kwargs)
        elif obj_type == "framework":
            ret = self.serialize_framework(o, **kwargs)
        elif obj_type == "report":
            ret = self.serialize_report(o, **kwargs)
        elif obj_type == "source":
            ret = self.serialize_source(o, **kwargs)
        elif obj_type == "scorecard":
            ret = self.serialize_scorecard(o, **kwargs)
        elif obj_type == "scorecardscore":
            ret = self.serialize_scorecardscore(o, **kwargs)
        elif obj_type == "criteria":
            ret = self.serialize_criteria(o, **kwargs)
        elif obj_type == "comment":
            ret = self.serialize_comment(o, **kwargs)
        elif obj_type == "inboxitem":
            ret = self.serialize_inboxitem(o, **kwargs)
        elif obj_type == "tag":
            ret = self.serialize_tag(o, **kwargs)
        if ret:
            ret["__type"] = obj_type
            return ret

        raise NotImplementedError("No serializer for %s" % obj_type)

    def serialize_user_dict(self):
        for obj_type, objs in self.user_data_to_serialize:
            for o in objs:
                self.serialized_objects[obj_type][o["ox_id"]] = self.serialize_obj(
                    obj_type, o
                )

    def fetch_all_user_data(self):
        all_known_user_ids = []
        #     * teams (cached on user)

        all_team_ids = (
            self.user.teammember_set.exclude(team__deleted=True)
            .distinct()
            .values_list("team_id", flat=True)
        )
        all_teams = (
            Team.objects.filter(id__in=all_team_ids)
            .all()
            .order_by("-created_at")
            .values(
                "id",
                "ox_id",
                "name",
                "description",
                "organization_id",
                # "members",
                "created_at",
                "modified_at",
            )
        )

        all_known_team_members = TeamMember.objects.filter(
            team__in=all_team_ids
        ).values(
            "user_id",
            "team_id",
            "can_view",
            "can_manage",
        )
        team_members_by_team = {}
        all_my_teams = []
        for tm in all_known_team_members:
            team_id = str(tm["team_id"])
            if team_id not in team_members_by_team:
                team_members_by_team[team_id] = []
            team_members_by_team[team_id].append(tm)
            if tm["user_id"] == self.user.id:
                all_my_teams.append(team_id)

            all_known_user_ids.append(tm["user_id"])

        #     add all users on team

        # #     * orgs (cached on user)
        all_org_ids = (
            self.user.organizationrole_set.exclude(organization__deleted=True)
            .distinct()
            .values_list("organization_id", flat=True)
        )
        all_organizations = Organization.objects.filter(id__in=all_org_ids).values(
            "id",
            "ox_id",
            "name",
            "description",
            # "members",
            "created_at",
            "modified_at",
        )

        all_known_org_members = []
        org_members_by_org = {}
        known_org_admin_ids = []
        all_my_orgs = []
        orgs_i_can_manage = {}

        all_known_org_members = OrganizationRole.objects.filter(
            organization__in=all_org_ids
        ).values(
            "user_id",
            "organization_id",
            "can_view",
            "can_manage",
        )
        for org_role in all_known_org_members:
            org_id = str(org_role["organization_id"])
            if org_role["user_id"] == self.user.id:
                all_my_orgs.append(org_id)
                if org_role["can_manage"]:
                    orgs_i_can_manage[org_id] = True

        for org_role in all_known_org_members:
            org_id = str(org_role["organization_id"])

            if org_role["can_manage"] or org_id in orgs_i_can_manage:
                if org_id not in org_members_by_org:
                    org_members_by_org[org_id] = []
                org_members_by_org[org_id].append(org_role)
            all_known_user_ids.append(org_role["user_id"])

            if org_role["can_manage"]:
                known_org_admin_ids.append(known_org_admin_ids)

        #     * gps
        all_gps = (
            GenericPermission.objects.filter(
                Q(
                    Q(can_score=True)
                    | Q(can_read=True)
                    | Q(can_write=True)
                    | Q(can_administer=True)
                )
                & Q(
                    Q(user=self.user)
                    | Q(user_id__in=all_known_user_ids)
                    | Q(team__in=self.user.teams)
                    | Q(organization__in=self.user.organizations)
                )
            )
            .all()
            .values(
                "id",
                "user_id",
                "organization_id",
                "team_id",
                "object_id",
                "content_type_id",
                "can_score",
                "can_read",
                "can_write",
                "can_administer",
            )
        )
        all_my_gps = (
            GenericPermission.objects.filter(
                Q(
                    Q(can_score=True)
                    | Q(can_read=True)
                    | Q(can_write=True)
                    | Q(can_administer=True)
                )
                & Q(
                    Q(user=self.user)
                    # | Q(user_id__in=all_known_user_ids)
                    | Q(team__in=self.user.teams)
                    | Q(organization__in=self.user.organizations)
                )
            )
            .all()
            .values_list(
                "id",
                flat=True,
            )
        )
        framework_gps = []
        framework_gp_ids = []
        all_framework_ids = []
        report_gps = []
        report_gp_ids = []
        all_report_ids = []
        source_gps = []
        source_gp_ids = []
        all_source_ids = []
        stack_gps = []
        stack_gp_ids = []
        all_stack_ids = []
        all_object_ids = []
        all_object_id_content_type_pairs = {}
        gps_by_holders = {
            "team": {},
            "user": {},
            "organization": {},
        }
        gps_by_objects = {
            "report": {},
            "stack": {},
            "source": {},
            "framework": {},
        }
        gps_by_ct_id = {}

        for gp in all_gps:
            all_object_ids.append(gp["object_id"])
            if str(gp["object_id"]) not in all_object_id_content_type_pairs:
                all_object_id_content_type_pairs[str(gp["object_id"])] = {}
            all_object_id_content_type_pairs[str(gp["object_id"])][
                str(gp["content_type_id"])
            ] = gp

            if gp["content_type_id"] == self.content_types["framework"]:
                if gp["id"] in all_my_gps:
                    framework_gps.append(gp)
                    framework_gp_ids.append(gp["object_id"])
                    all_framework_ids.append(gp["object_id"])
                if str(gp["object_id"]) not in gps_by_objects["framework"]:
                    gps_by_objects["framework"][str(gp["object_id"])] = []
                gps_by_objects["framework"][str(gp["object_id"])].append(gp)
            elif gp["content_type_id"] == self.content_types["report"]:
                if gp["id"] in all_my_gps:
                    report_gps.append(gp)
                    report_gp_ids.append(gp["object_id"])
                    all_report_ids.append(gp["object_id"])
                if str(gp["object_id"]) not in gps_by_objects["report"]:
                    gps_by_objects["report"][str(gp["object_id"])] = []
                gps_by_objects["report"][str(gp["object_id"])].append(gp)
            elif gp["content_type_id"] == self.content_types["source"]:
                if gp["id"] in all_my_gps:
                    source_gps.append(gp)
                    source_gp_ids.append(gp["object_id"])
                    all_source_ids.append(gp["object_id"])
                if str(gp["object_id"]) not in gps_by_objects["source"]:
                    gps_by_objects["source"][str(gp["object_id"])] = []
                gps_by_objects["source"][str(gp["object_id"])].append(gp)
            elif gp["content_type_id"] == self.content_types["stack"]:
                if gp["id"] in all_my_gps:
                    stack_gps.append(gp)
                    stack_gp_ids.append(gp["object_id"])
                    all_stack_ids.append(gp["object_id"])
                if str(gp["object_id"]) not in gps_by_objects["stack"]:
                    gps_by_objects["stack"][str(gp["object_id"])] = []
                gps_by_objects["stack"][str(gp["object_id"])].append(gp)

            if gp["team_id"]:
                if str(gp["team_id"]) not in gps_by_holders["team"]:
                    gps_by_holders["team"][str(gp["team_id"])] = []
                gps_by_holders["team"][str(gp["team_id"])].append(gp)
            if gp["user_id"]:
                if str(gp["user_id"]) not in gps_by_holders["user"]:
                    gps_by_holders["user"][str(gp["user_id"])] = []
                gps_by_holders["user"][str(gp["user_id"])].append(gp)
            if gp["organization_id"]:
                if str(gp["organization_id"]) not in gps_by_holders["organization"]:
                    gps_by_holders["organization"][str(gp["organization_id"])] = []
                gps_by_holders["organization"][str(gp["organization_id"])].append(gp)

            if str(gp["content_type_id"]) not in gps_by_ct_id:
                gps_by_ct_id[str(gp["content_type_id"])] = {}
            if str(gp["object_id"]) not in gps_by_ct_id[str(gp["content_type_id"])]:
                gps_by_ct_id[str(gp["content_type_id"])][str(gp["object_id"])] = []
            gps_by_ct_id[str(gp["content_type_id"])][str(gp["object_id"])].append(gp)

        #     * stacks (fetch reports as well)
        all_stacks = (
            Stack.objects.filter(id__in=stack_gp_ids)
            .annotate(
                report_ids=ArrayAgg("reports__id"),
            )
            .values(
                "id",
                "ox_id",
                "name",
                "subtitle",
                "notes",
                "report_ids",
                "created_at",
                "modified_at",
                "created_by_id",
                "modified_by_id",
            )
        )
        all_stacks_by_report = {}
        all_stacks_by_id = {}
        for s in all_stacks:
            for r_id in s["report_ids"]:
                if r_id not in all_report_ids:
                    all_report_ids.append(r_id)
                    if str(r_id) not in all_stacks_by_report:
                        all_stacks_by_report[str(r_id)] = []
                    all_stacks_by_report[str(r_id)].append(s["id"])
            all_known_user_ids.append(s["created_by_id"])
            all_known_user_ids.append(s["modified_by_id"])
            all_stacks_by_id[str(s["id"])] = s
            self.object_ids_to_ox_id["stacks"][str(s["id"])] = s["ox_id"]

        #     * reports (add stacks and gps)
        all_reports = (
            Report.objects.filter(id__in=all_report_ids)
            .annotate(
                source_ids=ArrayAgg("sources__id"),
            )
            .values(
                "source_ids",
                "id",
                "ox_id",
                "name",
                "subtitle",
                "created_by_id",
                "modified_by_id",
                "created_at",
                "modified_at",
                "notes",
                "ox_score",
                "has_skipped",
                "feedback_score",
                "feedback_comment",
            )
            .distinct()
        )
        for r in all_reports:
            all_known_user_ids.append(r["created_by_id"])
            all_known_user_ids.append(r["modified_by_id"])
            self.object_ids_to_ox_id["reports"][str(r["id"])] = r["ox_id"]
            for s_id in r["source_ids"]:
                if s_id:
                    all_source_ids.append(s_id)

        all_scorecards_data = Scorecard.objects.filter(
            report_id__in=all_report_ids
        ).values(
            "id",
            "ox_id",
            "report_id",
            "framework_id",
            "scorer_id",
            "ox_score",
            "has_skipped",
            "created_at",
            "modified_at",
        )

        all_scorecard_ids = []
        sc_by_report = {}
        sc_by_framework = {}
        sc_by_id = {}
        serialized_sc_by_framework = {}
        all_scorecards = []
        for sc in all_scorecards_data:
            if sc["framework_id"] not in all_framework_ids:
                all_framework_ids.append(sc["framework_id"])
            all_scorecard_ids.append(sc["id"])
            all_scorecards.append(sc)
            all_known_user_ids.append(sc["scorer_id"])

            sc_by_id[str(sc["id"])] = sc

        all_criteria_ids = []
        all_scorecard_scores = (
            ScorecardScore.objects.filter(scorecard_id__in=all_scorecard_ids)
            .values(
                "id",
                "ox_id",
                "scorecard_id",
                "score",
                "gpt_scored_last",
                "comment",
                "criteria_id",
                "created_at",
                "modified_at",
            )
            .order_by("-created_at")
        )

        scs_by_scorecard = {}
        scs_by_criteria = {}
        scs_by_scorer = {}
        for scs in all_scorecard_scores:
            if str(scs["criteria_id"]) not in scs_by_criteria:
                scs_by_criteria[str(scs["criteria_id"])] = []
            scs_by_criteria[str(scs["criteria_id"])].append(scs)

            scorer_id = str(sc_by_id[str(scs["scorecard_id"])]["scorer_id"])
            if scorer_id not in scs_by_scorer:
                scs_by_scorer[scorer_id] = []
            scs_by_scorer[scorer_id].append(scs)

        #     * frameworks (from GPs and scorecards)
        all_frameworks = (
            Framework.objects.filter(id__in=all_framework_ids)
            .annotate(
                criteria_ids=ArrayAgg("criteria__id"),
            )
            .values(
                "id",
                "ox_id",
                "name",
                "subtitle",
                "notes",
                "criteria_ids",
                "created_at",
                "modified_at",
                "created_by_id",
                "modified_by_id",
            )
        )
        for f in all_frameworks:
            all_known_user_ids.append(f["created_by_id"])
            all_known_user_ids.append(f["modified_by_id"])

        all_criteria_ids = []
        criteria_by_framework = {}
        all_criteria = Criteria.objects.filter(
            framework_id__in=all_framework_ids
        ).values(
            "id",
            "ox_id",
            "name",
            "description",
            "weight",
            "index",
            "framework_id",
            "created_at",
            "modified_at",
            "created_by_id",
            "modified_by_id",
        )
        for c in all_criteria:
            if str(c["framework_id"]) not in criteria_by_framework:
                criteria_by_framework[str(c["framework_id"])] = []
            criteria_by_framework[str(c["framework_id"])].append(c)

            all_known_user_ids.append(c["created_by_id"])
            all_known_user_ids.append(c["modified_by_id"])

        all_possible_comments = Comment.objects.filter(
            object_id__in=all_object_ids
        ).values(
            "id",
            "ox_id",
            "user_id",
            "object_id",
            "content_type_id",
            "body",
            "edited",
            # "react_url": self.react_url,
            # "vue_url": self.vue_url,
            "created_by_id",
            "created_at",
            "modified_at",
        )
        all_comments_by_ct_and_id = {}
        all_comments_by_id = {}
        all_comments = []
        for pc in all_possible_comments:
            if (
                str(pc["object_id"]) in all_object_id_content_type_pairs
                and str(pc["content_type_id"])
                in all_object_id_content_type_pairs[str(pc["object_id"])]
            ):
                all_comments.append(pc)
                all_known_user_ids.append(pc["user_id"])
                all_known_user_ids.append(pc["created_by_id"])

                if str(pc["content_type_id"]) not in all_comments_by_ct_and_id:
                    all_comments_by_ct_and_id[str(pc["content_type_id"])] = {}
                if (
                    str(pc["object_id"])
                    not in all_comments_by_ct_and_id[str(pc["content_type_id"])]
                ):
                    all_comments_by_ct_and_id[str(pc["content_type_id"])][
                        str(pc["object_id"])
                    ] = []
                all_comments_by_ct_and_id[str(pc["content_type_id"])][
                    str(pc["object_id"])
                ].append(pc)
                all_comments_by_id[str(pc["id"])] = pc

        all_source_ids = set(all_source_ids)
        all_sources = (
            Source.objects.filter(id__in=all_source_ids)
            .values(
                "id",
                "ox_id",
                "name",
                "subtitle",
                "notes",
                "created_by_id",
                "modified_by_id",
                "created_at",
                "modified_at",
            )
            .distinct()
        )
        for s in all_sources:
            all_known_user_ids.append(s["created_by_id"])
            all_known_user_ids.append(s["modified_by_id"])
            self.object_ids_to_ox_id["sources"][str(s["id"])] = s["ox_id"]

        all_possible_object_subscriptions = ObjectSubscription.objects.filter(
            object_id__in=all_object_ids
        ).values(
            "id",
            "user_id",
            "object_id",
            "content_type_id",
        )
        all_object_subscriptions = []
        all_object_subscriptions_by_ct_and_id = {}
        for pos in all_possible_object_subscriptions:
            obj_id = str(pos["object_id"])
            ct_id = str(pos["content_type_id"])
            if (
                obj_id in all_object_id_content_type_pairs
                and ct_id in all_object_id_content_type_pairs[obj_id]
            ):
                all_object_subscriptions.append(pos)
                if ct_id not in all_object_subscriptions_by_ct_and_id:
                    all_object_subscriptions_by_ct_and_id[ct_id] = {}
                if obj_id not in all_object_subscriptions_by_ct_and_id[ct_id]:
                    all_object_subscriptions_by_ct_and_id[ct_id][obj_id] = []
                all_object_subscriptions_by_ct_and_id[ct_id][obj_id].append(pos)
                all_known_user_ids.append(pos["user_id"])

        all_tag_ids = Tag.objects.filter(
            Q(user=self.user) | Q(organization_id__in=all_org_ids)
        ).values_list("id", flat=True)

        all_tags = Tag.objects.filter(id__in=all_tag_ids).values(
            "id",
            "ox_id",
            "name",
            "user_id",
            "organization_id",
            "created_at",
            "modified_at",
        )
        tags_by_id = {}
        for t in all_tags:
            tags_by_id[str(t["id"])] = t
            self.object_ids_to_ox_id["tags"][str(t["id"])] = t["ox_id"]

        all_tagged_objects = TaggedObject.objects.filter(tag__in=all_tag_ids).values(
            "id",
            "tag_id",
            "object_id",
            "content_type_id",
        )
        all_tagged_objs_by_ct_and_id = {}
        for tag in all_tagged_objects:
            ct = str(tag["content_type_id"])
            obj_id = str(tag["object_id"])
            tag_id = str(tag["id"])

            if ct not in all_tagged_objs_by_ct_and_id:
                all_tagged_objs_by_ct_and_id[ct] = {}

            if obj_id not in all_tagged_objs_by_ct_and_id[ct]:
                all_tagged_objs_by_ct_and_id[ct][obj_id] = []

            if tag_id not in all_tagged_objs_by_ct_and_id[ct][obj_id]:
                all_tagged_objs_by_ct_and_id[ct][obj_id].append(tag)

        all_known_user_ids.append(self.user.id)
        all_known_user_ids = set(all_known_user_ids)
        if None in all_known_user_ids:
            all_known_user_ids.remove(None)

        #     * users (from all of the above, save every time we serialize
        all_users = User.objects.filter(id__in=all_known_user_ids).values(
            "id",
            "ox_id",
            "first_name",
            "last_name",
            "username",
            "time_zone",
            "public_signup",
            "pinned_report_id",
            "pinned_framework_id",
            "pinned_stack_id",
        )

        all_inbox_items = (
            InboxItem.objects.filter(user=self.user, deleted=False)
            .all()
            .distinct()
            .values(
                "id",
                "ox_id",
                "content_type_id",
                "object_id",
                "comment_id",
                "user_id",
                "read",
                "done",
                "created_by_id",
                "created_at",
                "modified_at",
            )
        )

        all_users_by_id = {}

        all_my_object_subscriptions = ObjectSubscription.objects.filter(
            user=self.user
        ).values(
            "id",
            "user_id",
            "object_id",
            "content_type_id",
        )
        object_subscriptions_by_ct_and_id = {}
        for os in all_my_object_subscriptions:
            if str(os["content_type_id"]) not in object_subscriptions_by_ct_and_id:
                object_subscriptions_by_ct_and_id[str(os["content_type_id"])] = []
            object_subscriptions_by_ct_and_id[str(os["content_type_id"])].append(
                str(os["object_id"])
            )

        self.all_gps = all_gps
        self.all_my_gps = all_my_gps
        self.framework_gps = framework_gps
        self.framework_gp_ids = framework_gp_ids
        self.report_gps = report_gps
        self.report_gp_ids = report_gp_ids
        self.source_gps = source_gps
        self.source_gp_ids = source_gp_ids
        self.stack_gps = stack_gps
        self.stack_gp_ids = stack_gp_ids
        self.all_stacks_by_id = all_stacks_by_id
        self.all_stacks_by_report = all_stacks_by_report
        self.gps_by_holders = gps_by_holders
        self.gps_by_objects = gps_by_objects
        self.gps_by_ct_id = gps_by_ct_id
        self.all_framework_ids = all_framework_ids
        self.all_report_ids = all_report_ids
        self.all_source_ids = all_source_ids
        self.all_stack_ids = all_stack_ids
        self.all_criteria_ids = all_criteria_ids
        self.all_scorecard_ids = all_scorecard_ids
        self.all_known_user_ids = all_known_user_ids
        self.all_object_ids = all_object_ids
        self.all_object_id_content_type_pairs = all_object_id_content_type_pairs
        self.all_comments = all_comments
        self.all_comments_by_ct_and_id = all_comments_by_ct_and_id
        self.all_comments_by_id = all_comments_by_id
        self.all_my_object_subscriptions = all_my_object_subscriptions
        self.object_subscriptions_by_ct_and_id = object_subscriptions_by_ct_and_id
        self.all_object_subscriptions_by_ct_and_id = (
            all_object_subscriptions_by_ct_and_id
        )
        self.all_object_subscriptions = all_object_subscriptions
        self.all_tag_ids = all_tag_ids
        self.all_tags = all_tags
        self.all_tagged_objects = all_tagged_objects
        self.all_tagged_objs_by_ct_and_id = all_tagged_objs_by_ct_and_id
        self.tags_by_id = tags_by_id

        self.scs_by_scorecard = scs_by_scorecard
        self.scs_by_criteria = scs_by_criteria
        self.scs_by_scorer = scs_by_scorer
        self.sc_by_report = sc_by_report
        self.sc_by_framework = sc_by_framework
        self.sc_by_id = sc_by_id
        self.serialized_sc_by_framework = serialized_sc_by_framework
        self.criteria_by_framework = criteria_by_framework

        self.all_teams = all_teams
        self.all_organizations = all_organizations
        self.all_known_team_members = all_known_team_members
        self.team_members_by_team = team_members_by_team
        self.all_known_org_members = all_known_org_members
        self.all_my_orgs = all_my_orgs
        self.all_my_teams = all_my_teams
        self.org_members_by_org = org_members_by_org
        self.all_stacks = all_stacks
        self.all_reports = all_reports
        self.all_sources = all_sources
        self.all_scorecards = all_scorecards
        self.all_scorecard_scores = all_scorecard_scores
        self.all_frameworks = all_frameworks
        self.all_criteria = all_criteria
        self.all_comments = all_comments
        self.all_users = all_users
        self.all_inbox_items = all_inbox_items

        for f in all_frameworks:
            self.object_ids_to_ox_id["frameworks"][str(f["id"])] = f["ox_id"]

        for c in all_criteria:
            self.object_ids_to_ox_id["criterias"][str(c["id"])] = c["ox_id"]

        for u in all_users:
            self.object_ids_to_ox_id["users"][str(u["id"])] = u["ox_id"]
            all_users_by_id[u["id"]] = u

        self.all_users_by_id = all_users_by_id

        for t in self.all_teams:
            self.object_ids_to_ox_id["teams"][str(t["id"])] = t["ox_id"]

        self.object_ids_to_ox_id["organizations"] = {}
        for o in self.all_organizations:
            self.object_ids_to_ox_id["organizations"][str(o["id"])] = o["ox_id"]

        self.all_my_teams_by_ox_id = []
        for t in self.all_my_teams:
            self.all_my_teams_by_ox_id.append(self.object_ids_to_ox_id["teams"][str(t)])

        self.all_my_orgs_by_ox_id = []
        for o in self.all_my_orgs:
            self.all_my_orgs_by_ox_id.append(
                self.object_ids_to_ox_id["organizations"][str(o)]
            )

    def create_user_dict(self):
        #     * teams (cached on user)

        # Clean scorecards based on permissions.
        cleaned_scorecards = []
        cleaned_scorecard_ids = []
        cleaned_scorecardscores = []
        cleaned_sc_by_id = {}
        cleaned_sc_by_report = {}
        self.report_has_hidden_scorecards = {}

        for sc in self.all_scorecards:
            # If it's mine, or I have view permission on the report, or the stack the report is in.
            can_see = False

            r_id = str(sc["report_id"])
            if sc["scorer_id"] == self.user.pk:
                can_see = True

            if not can_see:
                perms = self.get_permissions("report", r_id)

                for k, p in perms.items():
                    if k == f"U-{self.user.ox_id}":
                        if p[1] == "1" or p[2] == "1" or p[3] == "1":
                            can_see = True
                            break
                    elif k[0] == "T":
                        team_id = k[2:]
                        if team_id in self.all_my_teams_by_ox_id and (
                            p[1] == "1" or p[2] == "1" or p[3] == "1"
                        ):
                            can_see = True
                            break
                    elif k[0] == "O":
                        org_id = k[2:]
                        if org_id in self.all_my_orgs_by_ox_id and (
                            p[1] == "1" or p[2] == "1" or p[3] == "1"
                        ):
                            can_see = True
                            break
            if not can_see:
                # Check stacks.
                if str(r_id) in self.all_stacks_by_report:
                    for s_id in self.all_stacks_by_report[str(r_id)]:
                        s_id = str(s_id)
                        perms = self.get_permissions("stack", s_id)

                        for k, p in perms.items():
                            if k == f"U-{self.user.ox_id}":
                                if p[1] == "1" or p[2] == "1" or p[3] == "1":
                                    can_see = True
                                    break
                            elif k[0] == "T":
                                team_id = k[2:]
                                if team_id in self.all_my_teams_by_ox_id and (
                                    p[1] == "1" or p[2] == "1" or p[3] == "1"
                                ):
                                    can_see = True
                                    break
                            elif k[0] == "O":
                                org_id = k[2:]
                                if org_id in self.all_my_orgs_by_ox_id and (
                                    p[1] == "1" or p[2] == "1" or p[3] == "1"
                                ):
                                    can_see = True
                                    break

            if can_see:
                cleaned_scorecards.append(sc)
                cleaned_scorecard_ids.append(sc["id"])
                cleaned_sc_by_id[str(sc["id"])] = sc
                if r_id not in cleaned_sc_by_report:
                    cleaned_sc_by_report[r_id] = []
                cleaned_sc_by_report[r_id].append(sc)
            else:
                self.report_has_hidden_scorecards[str(sc["report_id"])] = True

        self.scs_by_scorecard = {}
        self.scs_by_criteria = {}
        self.scs_by_scorer = {}
        for scs in self.all_scorecard_scores:
            if scs["scorecard_id"] in cleaned_scorecard_ids:
                if str(scs["criteria_id"]) not in self.scs_by_criteria:
                    self.scs_by_criteria[str(scs["criteria_id"])] = []
                self.scs_by_criteria[str(scs["criteria_id"])].append(scs)

                scorer_id = str(self.sc_by_id[str(scs["scorecard_id"])]["scorer_id"])
                if scorer_id not in self.scs_by_scorer:
                    self.scs_by_scorer[scorer_id] = []
                self.scs_by_scorer[scorer_id].append(scs)

                cleaned_scorecardscores.append(scs)

        self.all_scorecards = cleaned_scorecards
        self.all_scorecard_ids = cleaned_scorecard_ids
        self.all_scorecard_scores = cleaned_scorecardscores
        self.sc_by_id = cleaned_sc_by_id
        self.sc_by_report = {}

        for o in self.all_organizations:
            self.object_ids_to_ox_id["organizations"][str(o["id"])] = o["ox_id"]
            self.add_to_serialized(
                "organizations", o["ox_id"], self.serialize_from_dict("organization", o)
            )

        for t in self.all_teams:
            self.add_to_serialized(
                "teams", t["ox_id"], self.serialize_from_dict("team", t)
            )

        for s in self.all_stacks:
            s_dict = self.serialize_from_dict("stack", s)
            self.add_to_serialized("stacks", s["ox_id"], s_dict)

        for scs in self.all_scorecard_scores:
            if str(scs["scorecard_id"]) not in self.scs_by_scorecard:
                self.scs_by_scorecard[str(scs["scorecard_id"])] = []
            self.scs_by_scorecard[str(scs["scorecard_id"])].append(scs)

        for sc in self.all_scorecards:
            # Serialize the basic scorecard.
            sc_dict = self.serialize_from_dict("scorecard", sc)

            # Add in scorecard scores.
            sc_dict["scores"] = []
            for scs in self.scs_by_scorecard.get(str(sc["id"]), []):
                sc_dict["scores"].append(
                    self.serialize_from_dict(
                        "scorecardscore", scs, scorer_id=sc["scorer_id"]
                    )
                )
            sc_dict["scores"].sort(key=lambda x: x["created_at_ms"])

            if str(sc["report_id"]) not in self.sc_by_report:
                self.sc_by_report[str(sc["report_id"])] = []
            self.sc_by_report[str(sc["report_id"])].append(sc_dict)

            if str(sc["framework_id"]) not in self.serialized_sc_by_framework:
                self.serialized_sc_by_framework[str(sc["framework_id"])] = []
            if str(sc["framework_id"]) not in self.sc_by_framework:
                self.sc_by_framework[str(sc["framework_id"])] = []
            self.serialized_sc_by_framework[str(sc["framework_id"])].append(sc_dict)
            self.sc_by_framework[str(sc["framework_id"])].append(sc)

            # self.add_to_serialized("scorecards", sc["ox_id"], sc_dict)

        for c in self.all_criteria:
            c_dict = self.serialize_from_dict("criteria", c)
            self.add_to_serialized("criterias", c["ox_id"], c_dict)

        for r in self.all_reports:
            r_dict = self.serialize_from_dict("report", r)
            r_dict["scorecards"] = self.sc_by_report.get(str(r["id"]), [])
            self.add_to_serialized("reports", r["ox_id"], r_dict)

        for s in self.all_sources:
            s_dict = self.serialize_from_dict("source", s)
            self.add_to_serialized("sources", s["ox_id"], s_dict)

        for t in self.all_tags:
            t_dict = self.serialize_from_dict("tag", t)
            self.add_to_serialized("tags", t["ox_id"], t_dict)

        #     * frameworks (from GPs and scorecards)

        for f in self.all_frameworks:
            serialized_scorecards = self.serialized_sc_by_framework.get(
                str(f["id"]), []
            )
            scorecards = self.sc_by_framework.get(str(f["id"]), [])

            criteria = []
            for c in self.criteria_by_framework.get(str(f["id"]), []):
                criteria.append(self.rel_by_id("criterias", c["ox_id"]))
            #     c_dict = self.serialize_from_dict("criteria", c)
            #     criteria.append(c_dict)
            #     self.add_to_serialized("criterias", c["ox_id"], c_dict)
            # criteria.sort(key=lambda x: x["created_at_ms"])

            f_dict = self.serialize_from_dict(
                "framework",
                f,
                criteria=criteria,
                serialized_scorecards=serialized_scorecards,
                scorecards=scorecards,
            )
            self.add_to_serialized("frameworks", f["ox_id"], f_dict)

        # These are now serialized onto the objects themselves.
        # for c in self.all_comments:
        #     c_dict = self.serialize_from_dict("comment", c)
        #     self.add_to_serialized("comments", c["ox_id"], c_dict)

        #     * users (from all of the above, save every time we serialize
        for u in self.all_users:
            u_dict = self.serialize_from_dict("user", u)
            self.add_to_serialized("users", u["ox_id"], u_dict)

        for ii in self.all_inbox_items:
            ii_dict = self.serialize_from_dict("inboxitem", ii)
            self.add_to_serialized("inboxitems", ii["ox_id"], ii_dict)

    # fmt: off
    def serialize_stack(self, stack_dict, **kwargs):
        tags = self.get_tags("stack", stack_dict["id"])
        reports = []
        if stack_dict.get("report_ids")[0]:
            reports = [
                self.rel_by_id("reports", self.get_ox_id_from_object_id("reports", r_id)) for r_id in stack_dict.get("report_ids", [])
            ]

        ret = {
            "id": stack_dict["ox_id"],
            "name": stack_dict["name"],
            "subtitle": stack_dict["subtitle"],
            "notes": stack_dict["notes"],
            "created_by": self.rel_by_id("users", self.get_ox_id_from_user_id(stack_dict["created_by_id"])),
            "modified_by": self.rel_by_id("users", self.get_ox_id_from_user_id(stack_dict["modified_by_id"])),
            "created_at_ms": self.datetime_ms(stack_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(stack_dict["modified_at"]),
            "reports": reports,
            "comments": [self.serialize_comment(c) for c in self.get_comments("stack", stack_dict["id"])],
            "permissions": self.get_permissions("stack", stack_dict["id"]),
            "subscribed": self.is_subscribed("stack", stack_dict["id"]),
            "tags": [self.rel_by_id("tags", t["ox_id"]) for t in tags],
            "search_text": self.get_search_text("stack", stack_dict, tags=tags),
            # Statistics is currently unused on the frontend.  Add it back in if that changes!
            # # "statistics": stats,
            "subscribers": [
                self.rel_by_id("users", self.get_ox_id_from_user_id(u["user_id"]))
                for u in self.all_subscribers("stack", stack_dict["id"])
            ],
        }
        return ret

    def serialize_report(self, report_dict, **kwargs):
        tags = self.get_tags("report", report_dict["id"])
        source_ids = []
        for s_id in report_dict.get("source_ids", []):
            if s_id:
                source_ids.append(s_id)
        ox_score = report_dict["ox_score"]
        if ox_score:
            ox_score = round(ox_score)
        feedback_score = report_dict["feedback_score"]
        if feedback_score:
            feedback_score = round(feedback_score)

        ret = {
            "id": report_dict["ox_id"],
            "color_index": report_dict["id"] % 21,
            "name": report_dict["name"],
            "subtitle": report_dict["subtitle"],
            "notes": report_dict["notes"],
            "created_by": self.rel_by_id("users", self.get_ox_id_from_user_id(report_dict["created_by_id"])),
            "modified_by": self.rel_by_id("users", self.get_ox_id_from_user_id(report_dict["modified_by_id"])),
            "created_at_ms": self.datetime_ms(report_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(report_dict["modified_at"]),
            "ox_score": ox_score,
            "has_skipped": report_dict["has_skipped"],
            "feedback_score": feedback_score,
            "feedback_comment": report_dict["feedback_comment"],
            "sources": [self.rel_by_id("sources", self.get_ox_id_from_object_id("sources", id)) for id in source_ids],
            "stack_ids": [
                s["ox_id"] for s in self.all_related_to_object_in_field_list(self.all_stacks, "report_ids", report_dict["id"])
            ],
            # Handled by containing serializer code.
            # "scorecards": report_scorecards,
            "has_hidden_scorecards": str(report_dict["id"]) in self.report_has_hidden_scorecards,
            "permissions": self.get_permissions("report", report_dict["id"]),
            "subscribed": self.is_subscribed("report", report_dict["id"]),
            "tags": [self.rel_by_id("tags", t["ox_id"]) for t in tags],
            "comments": [self.serialize_comment(c) for c in self.get_comments("report", report_dict["id"])],
            "search_text": self.get_search_text("report", report_dict, tags=tags),
            "subscribers": [
                self.rel_by_id("users", self.get_ox_id_from_user_id(u["user_id"]))
                for u in self.all_subscribers("report", report_dict["id"])
            ],
        }
        return ret

    def serialize_framework(self, framework_dict, **kwargs):
        criteria = kwargs["criteria"]
        scorecards = kwargs["scorecards"]
        serialized_scorecards = kwargs["serialized_scorecards"]
        total_scores = 0
        num_scores = 0
        has_skipped = False
        scorers = {}
        reports = {}
        scores_by_criteria = {}
        report_feedback_scores = []
        for s in serialized_scorecards:
            if s["ox_score"] or s["ox_score"] == 0:
                total_scores += s["ox_score"]
                num_scores += 1
            if s["has_skipped"]:
                has_skipped = True

            scorers[str(s["scorer"])] = True
            if "scores" in s:
                for score in s["scores"]:
                    if score["score"] is not None:
                        if score["criteria"] not in scores_by_criteria:
                            scores_by_criteria[score["criteria"]] = []
                        scores_by_criteria[score["criteria"]].append(score["score"])

        for s in scorecards:
            reports[str(s["report_id"])] = True

        ox_score = None
        if num_scores > 0:
            ox_score = round(total_scores / num_scores)

        number_of_users = len(scorers.keys())
        report_id_list = list(reports.keys())
        number_of_reports = len(report_id_list)

        for r in self.all_reports:
            r_id = str(r["id"])
            if r_id in report_id_list and r["feedback_score"] is not None:
                report_feedback_scores.append(r["feedback_score"])

        average_feedback_score = None
        if len(report_feedback_scores) > 0:
            average_feedback_score = Decimal(sum(report_feedback_scores) / len(report_feedback_scores))

        highest_scoring_criterion = None
        highest_scoring_criterion_score = -1
        lowest_scoring_criterion = None
        lowest_scoring_criterion_score = 11
        for key, sbc in scores_by_criteria.items():
            avg_score = sum(sbc) / len(sbc)
            criteria_ox_id = key.split("'")[1]
            if avg_score > highest_scoring_criterion_score:
                highest_scoring_criterion_score = avg_score
                highest_scoring_criterion = criteria_ox_id
            if avg_score < lowest_scoring_criterion_score:
                lowest_scoring_criterion_score = avg_score
                lowest_scoring_criterion = criteria_ox_id

        if lowest_scoring_criterion:
            lowest_scoring_criterion = self.rel_by_id("criterias", lowest_scoring_criterion)
        if highest_scoring_criterion:
            highest_scoring_criterion = self.rel_by_id("criterias", highest_scoring_criterion)

        tags = self.get_tags("framework", framework_dict["id"])
        ret = {
            "id": framework_dict["ox_id"],
            "name": framework_dict["name"],
            "subtitle": framework_dict["subtitle"],
            "notes": framework_dict["notes"],

            "created_by": self.rel_by_id("users", self.get_ox_id_from_user_id(framework_dict["created_by_id"])),
            "modified_by": self.rel_by_id("users", self.get_ox_id_from_user_id(framework_dict["modified_by_id"])),
            "created_at_ms": self.datetime_ms(framework_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(framework_dict["modified_at"]),

            "ox_score": ox_score,
            "has_skipped": has_skipped,
            "number_of_users": number_of_users,
            "number_of_reports": number_of_reports,
            "average_feedback_score": average_feedback_score,

            "report_id_list": [self.get_ox_id_from_object_id("reports", r) for r in report_id_list],
            "highest_scoring_criterion": highest_scoring_criterion,
            "lowest_scoring_criterion": lowest_scoring_criterion,
            "criteria": criteria,

            # "statistics": stats,
            "permissions": self.get_permissions("framework", framework_dict["id"]),
            "subscribed": self.is_subscribed("framework", framework_dict["id"]),
            "tags": [self.rel_by_id("tags", t["ox_id"]) for t in tags],
            "comments": [
                self.serialize_comment(c)for c in self.get_comments("framework", framework_dict["id"])
            ],
            "search_text": self.get_search_text("framework", framework_dict, tags=tags),
            "subscribers": [
                self.rel_by_id("users", self.get_ox_id_from_user_id(u["user_id"]))
                for u in self.all_subscribers("framework", framework_dict["id"])
            ],
        }
        return ret

    def serialize_source(self, source_dict, **kwargs):
        tags = self.get_tags("source", source_dict["id"])

        ret = {
            "id": source_dict["ox_id"],
            "name": source_dict["name"],
            "subtitle": source_dict["subtitle"],
            "notes": source_dict["notes"],
            "created_by": self.rel_by_id("users", self.get_ox_id_from_user_id(source_dict["created_by_id"])),
            "modified_by": self.rel_by_id("users", self.get_ox_id_from_user_id(source_dict["modified_by_id"])),
            "created_at_ms": self.datetime_ms(source_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(source_dict["modified_at"]),
            "report_id_list": [
                r["ox_id"] for r in self.all_related_to_object_in_field_list(self.all_reports, "source_ids", source_dict["id"])
            ],

            "permissions": self.get_permissions("source", source_dict["id"]),
            "subscribed": self.is_subscribed("source", source_dict["id"]),
            "tags": [self.rel_by_id("tags", t["ox_id"]) for t in tags],
            "comments": [
                self.serialize_comment(c) for c in self.get_comments("source", source_dict["id"])
            ],
            "search_text": self.get_search_text("source", source_dict, tags=tags),
            "subscribers": [
                self.rel_by_id("users", self.get_ox_id_from_user_id(u["user_id"]))
                for u in self.all_subscribers("source", source_dict["id"])
            ],
        }

        return ret

    def serialize_scorecard(self, scorecard_dict, **kwargs):
        ret = {
            "id": scorecard_dict["ox_id"],
            "created_at_ms": self.datetime_ms(scorecard_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(scorecard_dict["modified_at"]),
            "scorer": self.rel_by_id("users", self.get_ox_id_from_user_id(scorecard_dict["scorer_id"])),
            "framework": self.rel_by_id(
                "frameworks", self.get_ox_id_from_object_id("frameworks", scorecard_dict["framework_id"]),
            ),
            "report_id": self.get_ox_id_from_object_id("reports", scorecard_dict["report_id"]),
            "ox_score": scorecard_dict["ox_score"],
            "has_skipped": scorecard_dict["has_skipped"],
            # "scores": [],
        }
        return ret

    def serialize_scorecardscore(self, scs_dict, **kwargs):
        scorer_id = self.get_ox_id_from_user_id(self.sc_by_id[str(scs_dict["scorecard_id"])]["scorer_id"])
        ret = {
            "id": scs_dict["ox_id"],
            "scorer": self.rel_by_id("users", scorer_id),
            "created_at_ms": self.datetime_ms(scs_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(scs_dict["modified_at"]),
            "score": scs_dict["score"],
            "gpt_scored_last": scs_dict["gpt_scored_last"],
            "comment": scs_dict["comment"],
            "criteria": self.rel_by_id("criterias", self.get_ox_id_from_object_id("criterias", scs_dict["criteria_id"])),
            # "criteria_id": scs_dict["criteria_id"],
        }
        return ret

    def serialize_criteria(self, criteria_dict, **kwargs):
        framework_criteria = self.criteria_by_framework[str(criteria_dict["framework_id"])]

        # Calculate relative_weight_as_percent, relative_weight_as_percent_of_max
        relative_weight_as_percent = None
        relative_weight_as_percent_of_max = None
        average_score = None
        total_weights = 0
        largest_weight = 0
        if not criteria_dict["weight"]:
            relative_weight_as_percent = 0
            relative_weight_as_percent_of_max = 0

        for c in framework_criteria:
            if c["weight"]:
                total_weights += c["weight"]
            if c["weight"] > largest_weight:
                largest_weight = c["weight"]

        if total_weights > 0:
            relative_weight_as_percent = 100 * criteria_dict["weight"] / total_weights

        if largest_weight > 0:
            relative_weight_as_percent_of_max = 100 * criteria_dict["weight"] / largest_weight

        # Calculate average_score
        total_scores = 0
        num_scores = 0
        total_user_scores = 0
        num_user_scores = 0
        average_score = None
        average_user_score = None
        id = str(criteria_dict["id"])
        if id in self.scs_by_criteria:
            for scs in self.scs_by_criteria[id]:
                if scs["score"]:
                    total_scores += scs["score"]
                    num_scores += 1
                    if self.sc_by_id[str(scs["scorecard_id"])]["scorer_id"] == self.user.id:
                        total_user_scores += scs["score"]
                        num_user_scores += 1
            if num_scores > 0:
                average_score = total_scores / num_scores
            if num_user_scores > 0:
                average_user_score = total_user_scores / num_user_scores

        weight = None
        if criteria_dict["weight"]:
            weight = round(criteria_dict["weight"])
        ret = {
            "id": criteria_dict["ox_id"],
            "name": criteria_dict["name"],
            "description": criteria_dict["description"],

            "weight": weight,
            "index": criteria_dict["index"],
            "relative_weight_as_percent": relative_weight_as_percent,
            "relative_weight_as_percent_of_max": relative_weight_as_percent_of_max,

            "average_score": average_score,
            "framework_pk": self.get_ox_id_from_object_id("frameworks", criteria_dict["framework_id"]),
            "created_by": self.rel_by_id("users", self.get_ox_id_from_user_id(criteria_dict["created_by_id"])),
            "created_at_ms": self.datetime_ms(criteria_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(criteria_dict["modified_at"]),
            "my_average_score": average_user_score,
        }
        return ret

    def serialize_comment(self, comment_dict, **kwargs):
        ret = {
            "id": comment_dict["ox_id"],
            "user": self.rel_by_id("users", self.get_ox_id_from_user_id(comment_dict["user_id"])),
            "body": comment_dict["body"],
            "edited": comment_dict["edited"],
            "created_by": self.rel_by_id("users", self.get_ox_id_from_user_id(comment_dict["created_by_id"])),
            "created_at_ms": self.datetime_ms(comment_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(comment_dict["modified_at"]),
        }
        return ret

    def serialize_tag(self, tag_dict, **kwargs):
        org = None
        if "organization_id" in tag_dict and tag_dict["organization_id"] is not None:
            org = self.rel_by_id("organizations", self.get_ox_id_from_object_id("organizations", tag_dict["organization_id"]))
        ret = {
            "id": tag_dict["ox_id"],
            "name": tag_dict["name"],
            "user": self.rel_by_id("users", self.get_ox_id_from_user_id(tag_dict["user_id"])),
            "organization": org,
            "created_at_ms": self.datetime_ms(tag_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(tag_dict["modified_at"]),
        }
        return ret

    def serialize_inboxitem(self, ii_dict, **kwargs):
        content_type_name = self.content_types_by_id[str(ii_dict["content_type_id"])]
        comment = self.all_comments_by_id[str(ii_dict["comment_id"])]

        ret = {
            "id": ii_dict["ox_id"],
            "type": content_type_name,
            "target": self.rel_by_id(
                f"{content_type_name}s",
                self.get_ox_id_from_object_id(f"{content_type_name}s", ii_dict["object_id"])
            ),
            # "comment": self.rel_by_id("comments", comment["ox_id"]),
            "comment": self.serialize_comment(comment),
            "user": self.rel_by_id("users", self.get_ox_id_from_user_id(ii_dict["user_id"])),
            # In the future, when inbox also updates for changes, this needs to go back to the deeper method on the model.
            "initiator": self.rel_by_id("users", self.get_ox_id_from_user_id(comment["user_id"])),
            # And this added "change_type": ii_dict["change_type"],
            "read": ii_dict["read"],
            "done": ii_dict["done"],

            "created_by": self.rel_by_id("users", self.get_ox_id_from_user_id(ii_dict["created_by_id"])),
            "created_at_ms": self.datetime_ms(ii_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(ii_dict["modified_at"]),

        }
        return ret

    def serialize_team(self, team_dict):
        last_admin_count = self.last_admin_for_count("team", team_dict["id"])
        members = [{
            "id": self.get_ox_id_from_user_id(tm["user_id"]),
            "can_view": tm["can_view"],
            "can_manage": tm["can_manage"],
        } for tm in self.team_members_by_team[str(team_dict["id"])]]
        ret = {
            "id": team_dict["ox_id"],
            "name": team_dict["name"],
            "description": team_dict["description"],
            "organization_id": team_dict["organization_id"],
            "organization": self.rel_by_id(
                "organizations",
                self.get_ox_id_from_object_id("organizations", str(team_dict["organization_id"]))
            ),
            "created_at_ms": self.datetime_ms(team_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(team_dict["modified_at"]),
            "members": members,
            "num_reports": self.get_gp_count(self.report_gps, "team", team_dict["id"]),
            "num_stacks": self.get_gp_count(self.stack_gps, "team", team_dict["id"]),
            "num_frameworks": self.get_gp_count(self.framework_gps, "team", team_dict["id"]),
            "num_sources": self.get_gp_count(self.source_gps, "team", team_dict["id"]),
            "last_admin_for_count": last_admin_count,
            "can_be_deleted": last_admin_count == 0,
        }
        return ret

    def serialize_organization(self, org_dict, **kwargs):
        last_admin_count = self.last_admin_for_count("organization", org_dict["id"])
        members = []
        if str(org_dict["id"]) in self.org_members_by_org:
            members = [{
                "id": self.get_ox_id_from_user_id(om["user_id"]),
                "can_view": om["can_view"],
                "can_manage": om["can_manage"],
            } for om in self.org_members_by_org[str(org_dict["id"])]]
        ret = {
            "id": org_dict["ox_id"],
            "name": org_dict["name"],
            "description": org_dict["description"],
            "created_at_ms": self.datetime_ms(org_dict["created_at"]),
            "modified_at_ms": self.datetime_ms(org_dict["modified_at"]),
            "members": members,
            "num_reports": self.get_gp_count(self.report_gps, "organization", org_dict["id"]),
            "num_stacks": self.get_gp_count(self.stack_gps, "organization", org_dict["id"]),
            "num_frameworks": self.get_gp_count(self.framework_gps, "organization", org_dict["id"]),
            "num_sources": self.get_gp_count(self.source_gps, "organization", org_dict["id"]),
            "last_admin_for_count": last_admin_count,
            "can_be_deleted": last_admin_count == 0,
        }

        return ret

    def serialize_user(self, user_dict, **kwargs):
        full_name = ""
        initials = ""
        if user_dict["first_name"]:
            full_name = user_dict["first_name"]
            initials += user_dict["first_name"][0]
        if user_dict["first_name"] and user_dict["last_name"]:
            full_name += " "
        if user_dict["last_name"]:
            full_name += user_dict["last_name"]
            initials += user_dict["last_name"][0]

        ret = {
            "id": user_dict["ox_id"],
            "username": user_dict["username"],
            "first_name": user_dict["first_name"],
            "last_name": user_dict["last_name"],
            "full_name": full_name,
            "initials": initials,
            "time_zone": user_dict["time_zone"],
            "public_signup": user_dict["public_signup"],
            "color_index": user_dict["id"] % 21,
            # Not sure this is needed.
            # "teams": [rel(t) for t in self.teams_requester_can_see(requesting_user)],
            # "organizations": [rel(o) for o in self.orgs_requester_can_see(requesting_user)],
        }
        return ret

    def serialize_my_user(self, user_dict, **kwargs):
        ret = self.serialize_user(user_dict, **kwargs)

        # if requesting_user == self:
        ret["pinned_report_pk"] = None
        ret["pinned_stack_pk"] = None
        ret["pinned_framework_pk"] = None
        if user_dict["pinned_report_id"]:
            try:
                ret["pinned_report_pk"] = self.get_ox_id_from_object_id("reports", str(user_dict["pinned_report_id"]))
            except:
                pass
        if user_dict["pinned_stack_id"]:
            try:
                ret["pinned_stack_pk"] = self.get_ox_id_from_object_id("stacks", str(user_dict["pinned_stack_id"]))
            except:
                pass
        if user_dict["pinned_framework_id"]:
            try:
                ret["pinned_framework_pk"] = self.get_ox_id_from_object_id("frameworks", str(user_dict["pinned_framework_id"]))
            except:
                pass

        user_averages = {"criteria": {}}
        avgs = {"criteria": {}}
        if str(user_dict["id"]) in self.scs_by_scorer:
            for scs in self.scs_by_scorer[str(user_dict["id"])]:
                if scs["score"] is not None:
                    criteria_pk = scs["criteria_id"]
                    if f"criteria__{criteria_pk}" not in avgs["criteria"]:
                        avgs["criteria"][f"criteria__{criteria_pk}"] = {}
                        avgs["criteria"][f"criteria__{criteria_pk}"]["num"] = 0
                        avgs["criteria"][f"criteria__{criteria_pk}"]["total"] = 0

                    avgs["criteria"][f"criteria__{criteria_pk}"]["total"] += scs["score"]
                    avgs["criteria"][f"criteria__{criteria_pk}"]["num"] += 1

        for k, c in avgs["criteria"].items():
            user_averages["criteria"][k] = c["total"] / c["num"]

        ret["email"] = self.user.email
        ret["averages"] = user_averages
        inbox = {
            "active": [],
            "done": [],
        }
        unread_count = 0
        for ii in self.all_inbox_items:
            ii_oxid = ii["ox_id"]
            if not ii["read"]:
                unread_count += 1
            if ii["done"]:
                inbox["done"].append(f"{ii_oxid}")
            else:
                inbox["active"].append(f"{ii_oxid}")

        inbox["unread_count"] = unread_count
        ret["inbox"] = inbox
        teams = []
        for t in self.all_my_teams:
            teams.append(self.rel_by_id("teams", self.get_ox_id_from_object_id("teams", t)),)
        organizations = []
        for o in self.all_my_orgs:
            organizations.append(self.rel_by_id("organizations", self.get_ox_id_from_object_id("organizations", o)),)

        ret["teams"] = teams
        ret["organizations"] = organizations
        return ret
    # fmt: on
