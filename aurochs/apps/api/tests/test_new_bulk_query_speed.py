# flake8: noqa
# from datetime import datetime
# import json
# import mock
# import unittest
# import pprint
# from django.test import TestCase
# from django.test import Client
# from django.db.models import Q
# from django.contrib.postgres.aggregates import ArrayAgg
# from django.contrib.contenttypes.models import ContentType
# from django.core.serializers.json import DjangoJSONEncoder
# from utils.factory import Factory
# from api.tests.base import EventTestCase
# from utils.helpers import rel, rel_by_id

# from frameworks.models import Criteria, Framework
# from organizations.models import (
#     Organization,
#     Team,
#     TeamMember,
#     User,
#     OrganizationRole,
#     Tag,
#     TaggedObject,
#     GenericPermission,
# )
# from reports.models import Report, Scorecard, ScorecardScore
# from sources.models import Source, SourceFeedback
# from stacks.models import Stack
# from collaboration.models import ObjectSubscription, Comment, InboxItem
# from history.models import ObjectHistoryChange
# from webapp.views import get_context

# # fmt: off
# REL_SPLIT_START = "__MAGIC_REL_SPLIT_START__"
# REL_SPLIT_END = "__MAGIC_REL_SPLIT_END__"

# NUM_OBJECTS = 2
# # NUM_OBJECTS = 3
# NUM_CRITERIA = 3


# def create_objs(user, obj_name, num_to_create, skip_permissions=False, *args, **kwargs):
#     objs = []
#     for i in range(0, num_to_create):
#         o = getattr(Factory, obj_name)(*args, user=user, **kwargs)
#         if not skip_permissions:
#             o.set_permission(
#                 acting_user=user,
#                 user=user,
#                 can_score=True,
#                 can_read=True,
#                 can_write=True,
#                 can_administer=True,
#             )
#             o.save()
#             objs.append(o)
#         else:
#             # Ignore password
#             objs.append(o[0])
#     return objs

# def is_subscribed(user, target, all_user_data):
#     for os in all_user_data["subscriptions"]:
#         # print(os)
#         if os.object_id == target.id: # && os.content_type == target.
#             return True
#     return False

# def all_of_gfk_in_user_objects(user_data, ct_id, related_type, obj):
#     related = []
#     # print(ct_id)
#     if user_data[related_type]:
#         for o in user_data[related_type]:
#             if obj.id == o["object_id"] and ct_id == o["content_type_id"]:
#                 related.append(o)
#     return related

# def all_of_type_in_user_objects(user_data, related_type, related_field, obj):
#     related = []
#     for o in user_data[related_type]:
#         # print(o)
#         # print(related_field)
#         if o[related_field] and obj["id"] in o[related_field]:
#             related.append(o)
#     return related

# def all_related_to_object(target_obj, search_type, related_field, all_user_objs):
#     found_list = []
#     for obj in all_user_objs[search_type]:
#         if related_field in obj and obj[related_field]["ox_id"] == target_obj["ox_id"]:
#             found_list.append(obj)
#     return found_list

# def datetime_ms(dt):
#     if dt:
#         return dt.timestamp() * 1000
#     return None

# def find_all_subscribers(object_id, content_type_id, all_user_data):
#     all_subs = []
#     for os in all_user_data["all_subscription_users"]:
#         if os["object_id"] == object_id and os["content_type_id"] == content_type_id and os["user_id"] != all_user_data["user"]["id"]:
#             all_subs.append(all_user_data["users_by_id"][os["user_id"]]["ox_id"])
#     return all_subs

# def search_text(obj, obj_type, ct, requesting_user, all_user_objs):
#     ox_id = obj["ox_id"]
#     text = f"{obj_type}:{ox_id}"
#     if obj["name"]:
#         text += "|name:" + obj["name"]

#     for t in all_of_gfk_in_user_objects(all_user_objs, ct, "tags", obj):
#         if t["name"]:
#             text += "|tag:" + t["name"]

#     if hasattr(obj, "stacks_ids"):
#         for s in all_of_gfk_in_user_objects(all_user_objs, ct, "stacks", obj):
#             if s.name:
#                 text += "|instk:" + s.name

#     if text != "":
#         return text + "|"
#     return text

# def get_permissions_obj(obj, ct_name, all_user_data):
#     perm_list = []
#     perms = {}
#     for gp in all_user_data[f"all_{ct_name}_gps"]:
#         # print("gp")
#         # print(gp)
#         if gp["object_id"] == obj["id"]:
#             id_str = ""
#             if gp["team_id"]:
#                 id_str = "T-%s" % gp["team_id"]
#             elif gp["user_id"]:
#                 id_str = "U-%s" % gp["user_id"]
#             elif gp["organization_id"]:
#                 id_str = "O-%s" % gp["organization_id"]

#             # print(id_str)
#             if id_str:
#                 perm_str = ""
#                 if gp["can_score"]:
#                     perm_str += "1"
#                 else:
#                     perm_str += "0"
#                 if gp["can_read"]:
#                     perm_str += "1"
#                 else:
#                     perm_str += "0"
#                 if gp["can_write"]:
#                     perm_str += "1"
#                 else:
#                     perm_str += "0"
#                 if gp["can_administer"]:
#                     perm_str += "1"
#                 else:
#                     perm_str += "0"
#                 perms[id_str] = perm_str
#             # perm_list.append()
#             # perms.append(gp)
#             #
#             # score read write admin
#             # {
#             #     'team-8lj;adsjfi': 0111,
#             # }
#             # perms[gp["user_id"]]

#     return perms

# def all_of_x_in_y_by_ox_id(source, target_ids):
#     found_list = []
#     for s in source:
#         if s["ox_id"] in target_ids:
#             found_list.push(s)
#     return found_list

# def all_related_to_object_on_field(obj_list, field, target, match_field="ox_id"):
#     found_list = []
#     for obj in obj_list:
#         if obj[field] == target[match_field]:
#             found_list.append(obj)
#     return found_list

# def all_related_to_object_in_field_list(obj_list, field, target, match_field="ox_id"):
#     found_list = []
#     for obj in obj_list:
#         if target[match_field] in obj[field]:
#             found_list.append(obj)
#     return found_list

# def ox_id_for_object_type_and_id(obj_type, id, all_user_data):
#     return all_user_data[obj_type]["ox_id"]


# class TestUpdatedStructureSpeed(EventTestCase):

#     def non_tes_t_omniserializer_speeds(self):
#         users = create_objs(self.user, "user", NUM_OBJECTS, skip_permissions=True)
#         teams = []
#         organizations = []
#         for i in range(0, NUM_OBJECTS):
#             o = Factory.organization()
#             t = Factory.team(organization=o)
#             teams.append(t)
#             organizations.append(o)
#         for u in users:
#             for t in teams:
#                 t.add_user(u)
#                 t.save()
#             for o in organizations:
#                 o.add_user(u)
#                 o.save()
#             frameworks = create_objs(u, "framework", NUM_OBJECTS)
#             reports = create_objs(u, "report", NUM_OBJECTS,)
#             sources = create_objs(u, "source", NUM_OBJECTS,)
#             stacks = create_objs(u, "stack", NUM_OBJECTS)
#             scorecards = []
#             scorecard_scores = []
#             for f in frameworks:
#                 for o in range(0, NUM_CRITERIA):
#                     Factory.criteria(framework=f)

#             for r in reports:
#                 for f in frameworks:
#                     sc = Factory.scorecard(report=r, framework=f, scorer=u)
#                     scorecards.append(sc)
#                     for c in f.criteria:
#                         scorecard_scores.append(
#                             Factory.scorecard_score(scorecard=sc, user=u, criteria=c)
#                         )
#                 for s in sources:
#                     r.sources.add(s)
#                 r.save()

#             for s in stacks:
#                 for r in reports:
#                     s.reports.add(r)

#         self.assertEqual(len(reports), NUM_OBJECTS)

#         start = datetime.now()
#         from organizations.serializers import OmniSerializer
#         s = OmniSerializer(u)
#         pprint.pprint(s.serialize())
#         end = datetime.now()
#         print(f"OmniSerializer time: {1000 * (end - start).total_seconds()} ms\n\n")
#         # print(s.serialize_to_json())

#     # def test_skip_orm_speeds(self):
#     #     users = create_objs(self.user, "user", NUM_OBJECTS, skip_permissions=True)
#     #     teams = []
#     #     organizations = []
#     #     for i in range(0, NUM_OBJECTS):
#     #         o = Factory.organization()
#     #         t = Factory.team(organization=o)
#     #         teams.append(t)
#     #         organizations.append(o)
#     #     for u in users:
#     #         for t in teams:
#     #             t.add_user(u)
#     #             t.save()
#     #         for o in organizations:
#     #             o.add_user(u)
#     #             o.save()
#     #         frameworks = create_objs(u, "framework", NUM_OBJECTS)
#     #         reports = create_objs(u, "report", NUM_OBJECTS,)
#     #         sources = create_objs(u, "source", NUM_OBJECTS,)
#     #         stacks = create_objs(u, "stack", NUM_OBJECTS)
#     #         scorecards = []
#     #         scorecard_scores = []
#     #         for f in frameworks:
#     #             for o in range(0, NUM_CRITERIA):
#     #                 Factory.criteria(framework=f)

#     #         for r in reports:
#     #             for f in frameworks:
#     #                 sc = Factory.scorecard(report=r, framework=f, scorer=u)
#     #                 scorecards.append(sc)
#     #                 for c in f.criteria:
#     #                     scorecard_scores.append(
#     #                         Factory.scorecard_score(scorecard=sc, user=u, criteria=c)
#     #                     )
#     #             for s in sources:
#     #                 r.sources.add(s)
#     #             r.save()

#     #         for s in stacks:
#     #             for r in reports:
#     #                 s.reports.add(r)

#     #     self.assertEqual(len(reports), NUM_OBJECTS)

#     #     start_new = datetime.now()
#     #     # all_gps = GenericPermission.objects.filter(Q(user=u) | Q(team__in=u.teams) | Q(organization__in=u.organizations)).all().prefetch_related("report", "stack", "framework", "source").values()
#     #     report_ct = ContentType.objects.get_for_model(Report)
#     #     report_gps = GenericPermission.objects.filter(
#     #         Q(content_type=report_ct)
#     #         & Q(
#     #             Q(can_score=True)
#     #             | Q(can_read=True)
#     #             | Q(can_write=True)
#     #             | Q(can_administer=True)
#     #         )
#     #         & Q(
#     #             Q(user=u)
#     #             | Q(team__in=u.teams)
#     #             | Q(organization__in=u.organizations)
#     #         )
#     #     ).all()
#     #     all_report_gp_ids = report_gps.values_list("object_id", flat=True)
#     #     all_report_gps = GenericPermission.objects.filter(
#     #         Q(content_type=report_ct)
#     #     ).all().values("object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id")

#     #     all_reports = (
#     #         Report.objects.filter(id__in=all_report_gp_ids)
#     #         .annotate(sources_ids=ArrayAgg('sources__id'),)
#     #         .values(
#     #             "sources_ids",
#     #             "id",
#     #             "ox_id",
#     #             "name",
#     #             "subtitle",
#     #             "created_by_id",
#     #             "modified_by_id",
#     #             "created_at",
#     #             "modified_at",
#     #             "notes",
#     #             "ox_score",
#     #             "has_skipped",
#     #             "feedback_score",
#     #             "feedback_comment",
#     #         ).distinct()
#     #     )
#     #     # print("\n\nall_reports")
#     #     # print(all_reports)

#     #     source_ct = ContentType.objects.get_for_model(Source)
#     #     # all_source_gps = (
#     #     #     GenericPermission.objects.filter(
#     #     #         Q(content_type=source_ct)
#     #     #         & Q(
#     #     #             Q(can_score=True)
#     #     #             | Q(can_read=True)
#     #     #             | Q(can_write=True)
#     #     #             | Q(can_administer=True)
#     #     #         )
#     #     #         & Q(
#     #     #             Q(user=u)
#     #     #             | Q(team__in=u.teams)
#     #     #             | Q(organization__in=u.organizations)
#     #     #         )
#     #     #     )
#     #     #     .all()
#     #     #     .values_list("object_id", flat=True)
#     #     # )

#     #     source_gps = GenericPermission.objects.filter(
#     #         Q(content_type=source_ct)
#     #         & Q(
#     #             Q(can_score=True)
#     #             | Q(can_read=True)
#     #             | Q(can_write=True)
#     #             | Q(can_administer=True)
#     #         )
#     #         & Q(
#     #             Q(user=u)
#     #             | Q(team__in=u.teams)
#     #             | Q(organization__in=u.organizations)
#     #         )
#     #     ).all()
#     #     all_source_gp_ids = source_gps.values_list("object_id", flat=True)
#     #     all_source_gps = GenericPermission.objects.filter(
#     #         Q(content_type=source_ct)
#     #     ).all().values("object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id")

#     #     all_sources = Source.objects.filter(id__in=all_source_gp_ids).values()

#     #     framework_ct = ContentType.objects.get_for_model(Framework)
#     #     # all_framework_gps = (
#     #     #     GenericPermission.objects.filter(
#     #     #         Q(content_type=framework_ct)
#     #     #         & Q(
#     #     #             Q(can_score=True)
#     #     #             | Q(can_read=True)
#     #     #             | Q(can_write=True)
#     #     #             | Q(can_administer=True)
#     #     #         )
#     #     #         & Q(
#     #     #             Q(user=u)
#     #     #             | Q(team__in=u.teams)
#     #     #             | Q(organization__in=u.organizations)
#     #     #         )
#     #     #     )
#     #     #     .all()
#     #     #     .values_list("object_id", flat=True)
#     #     # )
#     #     framework_gps = GenericPermission.objects.filter(
#     #         Q(content_type=framework_ct)
#     #         & Q(
#     #             Q(can_score=True)
#     #             | Q(can_read=True)
#     #             | Q(can_write=True)
#     #             | Q(can_administer=True)
#     #         )
#     #         & Q(
#     #             Q(user=u)
#     #             | Q(team__in=u.teams)
#     #             | Q(organization__in=u.organizations)
#     #         )
#     #     ).all()
#     #     all_framework_gp_ids = framework_gps.values_list("object_id", flat=True)
#     #     all_framework_gps = GenericPermission.objects.filter(
#     #         Q(content_type=framework_ct)
#     #     ).all().values("object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id")

#     #     all_frameworks = Framework.objects.filter(id__in=all_framework_gp_ids).annotate(
#     #         criteria_ids=ArrayAgg('criteria__id'),
#     #     ).values(
#     #         "id",
#     #         "ox_id",
#     #         "name",
#     #         "subtitle",
#     #         "notes",
#     #         "criteria_ids",
#     #         "created_at",
#     #         "modified_at",
#     #         "created_by_id",
#     #         "modified_by_id",
#     #     )

#     #     all_criteria = Criteria.objects.filter(framework_id__in=all_framework_gp_ids).values(
#     #         "id",
#     #         "ox_id",
#     #         "name",
#     #         "description",
#     #         "weight",
#     #         "index",
#     #         "created_at",
#     #         "modified_at",
#     #         "created_by_id",
#     #         "modified_by_id",
#     #     )
#     #     all_criteria_by_id = {}
#     #     for c in all_criteria:
#     #         all_criteria_by_id[str(c['id'])] = c

#     #     stack_ct = ContentType.objects.get_for_model(Stack)

#     #     stack_gps = GenericPermission.objects.filter(
#     #         Q(content_type=stack_ct)
#     #         & Q(
#     #             Q(can_score=True)
#     #             | Q(can_read=True)
#     #             | Q(can_write=True)
#     #             | Q(can_administer=True)
#     #         )
#     #         & Q(
#     #             Q(user=u)
#     #             | Q(team__in=u.teams)
#     #             | Q(organization__in=u.organizations)
#     #         )
#     #     ).all()
#     #     all_stack_gp_ids = stack_gps.values_list("object_id", flat=True)
#     #     all_stack_gps = GenericPermission.objects.filter(
#     #         Q(content_type=stack_ct)
#     #     ).all().values(
#     #         "object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id",
#     #     )

#     #     all_stacks = Stack.objects.filter(id__in=all_stack_gp_ids).annotate(
#     #         reports_ids=ArrayAgg('reports__id'),
#     #     ).values(
#     #         "id",
#     #         "ox_id",
#     #         "name",
#     #         "subtitle",
#     #         "notes",
#     #         "reports_ids",
#     #         "created_at",
#     #         "modified_at",
#     #         "created_by_id",
#     #         "modified_by_id",
#     #     )

#     #     all_scorecards = Scorecard.objects.filter(report_id__in=all_report_gp_ids)
#     #     # all_scorecards_ids = all_scorecards.values_list("id", flat=True)
#     #     all_scorecards = all_scorecards.values(
#     #         "id",
#     #         "ox_id",
#     #         "report_id",
#     #         "framework_id",
#     #         "scorer_id",
#     #         "created_at",
#     #         "modified_at",
#     #     )
#     #     # print(all_scorecards)
#     #     all_scorecards_ids = [o["id"] for o in all_scorecards]
#     #     # print(all_scorecards_ids)
#     #     # print(ScorecardScore.objects.all())
#     #     all_scorecard_scores = ScorecardScore.objects.filter(scorecard_id__in=all_scorecards_ids).values(
#     #         "id",
#     #         "ox_id",
#     #         "scorecard_id",
#     #         "score",
#     #         "comment",
#     #         "criteria_id",
#     #         "created_at",
#     #         "modified_at",
#     #     )
#     #     # print(all_scorecard_scores)

#     #     all_team_people = (
#     #         TeamMember.objects.filter(team__in=u.teams)
#     #         .prefetch_related("user", "team")
#     #         .values()
#     #     )
#     #     all_org_people = (
#     #         OrganizationRole.objects.filter(organization__in=u.organizations)
#     #         .prefetch_related("user", "organization")
#     #         .values()
#     #     )
#     #     all_inboxitems = (
#     #         InboxItem.objects.filter(user=u).prefetch_related("comment").values()
#     #     )
#     #     all_subscriptions = ObjectSubscription.objects.filter(user=u).values()
#     #     all_tags = Tag.objects.filter(Q(user=u)| Q(organization__in=u.organizations)).values()
#     #     all_tagged_objects = TaggedObject.objects.filter(tag__in=all_tags).values()

#     #     gps = (
#     #         GenericPermission.objects.filter(
#     #             Q(
#     #                 Q(can_score=True)
#     #                 | Q(can_read=True)
#     #                 | Q(can_write=True)
#     #                 | Q(can_administer=True)
#     #             )
#     #             & Q(
#     #                 Q(user=u)
#     #                 | Q(team__in=u.teams)
#     #                 | Q(organization__in=u.organizations)
#     #             )
#     #         )
#     #         .all()
#     #         .values_list(
#     #             "object_id",
#     #             "content_type_id",
#     #             "can_score",
#     #             "can_read",
#     #             "can_write",
#     #             "can_administer",
#     #         )
#     #     )
#     #     cts = ContentType.objects.all().values("id", "app_label", "model")
#     #     ct_framework_id = None
#     #     ct_report_id = None
#     #     ct_source_id = None
#     #     ct_stack_id = None
#     #     for ct in cts:
#     #         if ct["model"] == "framework":
#     #             ct_framework_id = ct["id"]
#     #         if ct["model"] == "report":
#     #             ct_report_id = ct["id"]
#     #         if ct["model"] == "source":
#     #             ct_source_id = ct["id"]
#     #         if ct["model"] == "stack":
#     #             ct_stack_id = ct["id"]
#     #     cts_shortcuts = {
#     #         "framework": ct_framework_id,
#     #         "report": ct_report_id,
#     #         "source": ct_source_id,
#     #         "stack": ct_stack_id,
#     #     }


#     #     all_subscription_users = ObjectSubscription.objects.filter(
#     #         Q(object_id__in=all_framework_gp_ids, content_type_id=ct_framework_id) |
#     #         Q(object_id__in=all_report_gp_ids, content_type_id=ct_report_id) |
#     #         Q(object_id__in=all_source_gp_ids, content_type_id=ct_source_id) |
#     #         Q(object_id__in=all_stack_gp_ids, content_type_id=ct_stack_id)
#     #     ).values_list('user_id', "object_id", "content_type_id")

#     #     all_comments = Comment.objects.filter(
#     #         Q(object_id__in=all_framework_gp_ids, content_type_id=ct_framework_id) |
#     #         Q(object_id__in=all_report_gp_ids, content_type_id=ct_report_id) |
#     #         Q(object_id__in=all_source_gp_ids, content_type_id=ct_source_id) |
#     #         Q(object_id__in=all_stack_gp_ids, content_type_id=ct_stack_id)
#     #     ).values('user_id', "object_id", "content_type_id", "body", "edited")

#     #     # all_{ct_name}_gps
#     #     users_i_know_about_ids = []
#     #     for gp in all_report_gps:
#     #         if gp["user_id"]:
#     #             users_i_know_about_ids.append(gp["user_id"])
#     #     for gp in all_framework_gps:
#     #         if gp["user_id"]:
#     #             users_i_know_about_ids.append(gp["user_id"])
#     #     for gp in all_source_gps:
#     #         if gp["user_id"]:
#     #             users_i_know_about_ids.append(gp["user_id"])
#     #     for gp in all_stack_gps:
#     #         if gp["user_id"]:
#     #             users_i_know_about_ids.append(gp["user_id"])
#     #     users_i_know_about = User.objects.filter(id__in=users_i_know_about_ids).values(
#     #         "id",
#     #         "ox_id",
#     #         "first_name",
#     #         "last_name",
#     #         "username",
#     #     )
#     #     users_i_know_about_by_id = {}
#     #     users_i_know_about_by_ox_id = {}
#     #     for user in users_i_know_about:
#     #         user["full_name"] = "%s %s" % (user['first_name'], user['last_name'])
#     #         users_i_know_about_by_id[f"{user['id']}"] = u
#     #         cleaned_user = user
#     #         del cleaned_user["id"]
#     #         users_i_know_about_by_ox_id[f"{user['ox_id']}"] = cleaned_user

#     #     all_objs_legacy_js = []
#     #     all_user_objs = {
#     #         # "user": u,
#     #         "reports": [],
#     #         "frameworks": [],
#     #         "criteria": [],
#     #         "sources": [],
#     #         "stacks": [],
#     #         "inboxitems": [],
#     #         "teams": [],
#     #         "tags": [],
#     #         "comments": all_comments,
#     #         "tagged_objects": all_tagged_objects,
#     #         "organizations": [],
#     #         "all_gps": gps,
#     #         "all_report_gp_ids": all_report_gp_ids,
#     #         "all_report_gps": all_report_gps,
#     #         "all_framework_gp_ids": all_framework_gp_ids,
#     #         "all_framework_gps": all_framework_gps,
#     #         "all_source_gp_ids": all_source_gp_ids,
#     #         "all_source_gps": all_source_gps,
#     #         "all_stack_gp_ids": all_stack_gp_ids,
#     #         "all_stack_gps": all_stack_gps,
#     #         "scorecards": all_scorecards,
#     #         "scorecard_scores": all_scorecard_scores,
#     #         "content_types": cts,
#     #         "cts_shortcuts": cts_shortcuts,
#     #         "subscriptions": all_subscriptions,
#     #         "all_subscription_users": all_subscription_users,
#     #         "users_by_id": users_i_know_about_by_id,
#     #     }
#     #     for obj in all_reports:
#     #         all_user_objs["reports"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_frameworks:
#     #         all_user_objs["frameworks"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_criteria:
#     #         all_user_objs["criteria"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_sources:
#     #         all_user_objs["sources"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_stacks:
#     #         all_user_objs["stacks"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_inboxitems:
#     #         all_user_objs["inboxitems"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_team_people:
#     #         all_user_objs["teams"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_org_people:
#     #         all_user_objs["organizations"].append(obj)
#     #         all_objs_legacy_js.append(obj)

#     #     for obj in all_tags:
#     #         all_user_objs["tags"].append(obj)
#     #         all_objs_legacy_js.append(obj)


#     #     # "subscribers": [rel_by_id(u, "ox_id") for u in s["subscribers"]],

#     #     # generate_js_data(all_user_objs, requesting_user=u)
#     #     print(all_user_objs["stacks"])
#     #     end_new = datetime.now()
#     #     all_user_output_data = {
#     #         # "user": u,
#     #         "reports": [],
#     #         "frameworks": [],
#     #         "criteria": [],
#     #         "sources": [],
#     #         "stacks": [],
#     #         "inboxitems": [],
#     #         "tags": [],
#     #         "comments": [],
#     #         "users": [],
#     #         "organizations": [],
#     #         "teams": [],
#     #         "subscriptions": [],
#     #         # "scorecards": all_scorecards,
#     #         # "scorecardscores": all_scorecard_scores,
#     #         "users_by_id": users_i_know_about_by_ox_id,
#     #     }
#     #     # print(users_i_know_about_by_id)
#     #     for r in all_reports:
#     #         all_scorecards = all_related_to_object_on_field(all_user_objs["scorecards"], "report_id", r, "id")
#     #         report_scorecards = []
#     #         for sc_data in all_scorecards:
#     #             sc = {
#     #                 "created_at_ms": datetime_ms(sc_data["created_at"]),
#     #                 "modified_at_ms": datetime_ms(sc_data["modified_at"]),
#     #                 "scorer": rel_by_id("users", users_i_know_about_by_id[str(sc_data["scorer_id"])].ox_id),
#     #                 "framework": rel_by_id("frameworks", sc_data["framework_id"]),
#     #                 "scores": [],
#     #             }
#     #             all_scorecard_scores = all_related_to_object_on_field(all_user_objs["scorecard_scores"], "scorecard_id", sc_data, "id")
#     #             for scs in all_scorecard_scores:

#     #                 score = {
#     #                     "ox_id": scs["ox_id"],
#     #                     "scorer": rel_by_id("users", users_i_know_about_by_id[str(sc_data["scorer_id"])].ox_id),
#     #                     "created_at_ms": datetime_ms(scs["created_at"]),
#     #                     "modified_at_ms": datetime_ms(scs["modified_at"]),
#     #                     "score": scs["score"],
#     #                     "comment": scs["comment"],
#     #                     "criteria": rel_by_id("criteria", all_criteria_by_id[str(scs["criteria_id"])]["ox_id"]),

#     #                 }
#     #                 sc["scores"].append(score)
#     #             report_scorecards.append(sc)

#     #         # print(all_related_to_object_in_field_list(all_user_objs["stacks"], "reports_ids", r, "id"))

#     #         all_user_output_data["reports"].append(
#     #             {
#     #                 # "id": r["id"],
#     #                 "ox_id": r["ox_id"],
#     #                 "name": r["name"],
#     #                 "subtitle": r["subtitle"],
#     #                 "notes": r["notes"],
#     #                 "created_by": rel_by_id("users", users_i_know_about_by_id[str(r["created_by_id"])].ox_id),
#     #                 "modified_by": rel_by_id("users", users_i_know_about_by_id[str(r["modified_by_id"])].ox_id),
#     #                 "created_at_ms": datetime_ms(r["created_at"]),
#     #                 "modified_at_ms": datetime_ms(r["modified_at"]),
#     #                 "ox_score": r["ox_score"],
#     #                 "has_skipped": r["has_skipped"],
#     #                 "feedback_score": r["feedback_score"],
#     #                 "feedback_comment": r["feedback_comment"],

#     #                 # Frameworks shouldn't be here.
#     #                 # "frameworks": [ rel_by_id("frameworks", f["ox_id"]) for f in all_of_x_in_y_by_ox_id(all_user_objs["frameworks"], r["frameworks_ids"])],
#     #                 # We don't use statistics.
#     #                 # "statistics": stats,

#     #                 "sources": [ rel_by_id("sources", s["ox_id"]) for s in all_of_type_in_user_objects(all_user_objs, "reports", "sources_ids", r,)],
#     #                 "stack_ids": [ s["ox_id"] for s in all_related_to_object_in_field_list(all_user_objs["stacks"], "reports_ids", r, "id")],
#     #                 "scorecards": report_scorecards,

#     #                 "permissions": get_permissions_obj(r, "report", all_user_objs),
#     #                 "subscribed": is_subscribed(u, s, all_user_objs),
#     #                 "tags": [rel_by_id("tags", t["ox_id"]) for t in all_of_gfk_in_user_objects(all_user_objs, ct_report_id, "tags", r,)],
#     #                 "comments": [rel_by_id("comments", t["ox_id"]) for c in all_of_gfk_in_user_objects(all_user_objs, ct_report_id, "comments", r,)],
#     #                 "subscribers": [rel_by_id("users", user_id) for user_id in find_all_subscribers(r["id"], ct_report_id, all_user_objs)],
#     #                 "search_text": search_text(r, "report", ct_report_id, u, all_user_objs),
#     #             }
#     #         )
#     #     for s in all_sources:
#     #         all_user_output_data["sources"].append(
#     #             {
#     #                 # "id": s["id"],
#     #                 "ox_id": s["ox_id"],
#     #                 "name": s["name"],
#     #                 "subtitle": s["subtitle"],
#     #                 "notes": s["notes"],
#     #                 "created_by": rel_by_id("users", s["created_by_id"]),
#     #                 "modified_by": rel_by_id("users", s["modified_by_id"]),
#     #                 "created_at_ms": datetime_ms(s["created_at"]),
#     #                 "modified_at_ms": datetime_ms(s["modified_at"]),
#     #                 "permissions": get_permissions_obj(s, "source", all_user_objs),
#     #                 "report_id_list": [ r["ox_id"] for r in all_of_type_in_user_objects(all_user_objs, "reports", "sources_ids", s,)],
#     #                 "subscribed": is_subscribed(u, s, all_user_objs),
#     #                 "tags": [rel_by_id("tags", t["ox_id"]) for t in all_of_gfk_in_user_objects(all_user_objs, ct_source_id, "tags", s,)],
#     #                 "comments": [rel_by_id("comments", t["ox_id"]) for c in all_of_gfk_in_user_objects(all_user_objs, ct_source_id, "comments", s,)],
#     #                 "subscribers": [rel_by_id("users", user_id) for user_id in find_all_subscribers(s["id"], ct_source_id, all_user_objs)],
#     #                 "search_text": search_text(s, "source", ct_source_id, u, all_user_objs),
#     #             }
#     #         )

#     #     for s in all_frameworks:
#     #         all_user_output_data["frameworks"].append(
#     #             {

#     #             }
#     #         )

#     #     for s in all_stacks:
#     #         all_user_output_data["stacks"].append(
#     #             {

#     #             }
#     #         )

#     #     # pprint.pprint([Source.values_dict_to_data(s, u, all_user_objs) for s in all_sources])
#     #     # pprint.pprint(all_user_output_data)
#     #     ret = json.dumps(all_user_output_data, sort_keys=True, cls=DjangoJSONEncoder,)
#     #     ret = ret.replace(f'"{REL_SPLIT_START}', "")
#     #     ret = ret.replace(f'{REL_SPLIT_END}"', "")
#     #     ret = ret.replace(f"{REL_SPLIT_START}", "")
#     #     ret = ret.replace(f"{REL_SPLIT_END}", "")
#     #     print(ret)
#     #     print(f"New time: {1000* (end_new - start_new).total_seconds()} ms\n\n")

#     # # def test_middle_way_speeds(self):
#     # #     users = create_objs(self.user, "user", NUM_OBJECTS, skip_permissions=True)
#     # #     teams = []
#     # #     organizations = []
#     # #     for i in range(0, NUM_OBJECTS):
#     # #         o = Factory.organization()
#     # #         t = Factory.team(organization=o)
#     # #         teams.append(t)
#     # #         organizations.append(o)
#     # #     for u in users:
#     # #         for t in teams:
#     # #             t.add_user(u)
#     # #             t.save()
#     # #         for o in organizations:
#     # #             o.add_user(u)
#     # #             o.save()
#     # #         frameworks = create_objs(u, "framework", NUM_OBJECTS)
#     # #         reports = create_objs(u, "report", NUM_OBJECTS)
#     # #         sources = create_objs(u, "source", NUM_OBJECTS)
#     # #         stacks = create_objs(u, "stack", NUM_OBJECTS)
#     # #         scorecards = []
#     # #         scorecard_scores = []
#     #         # for f in frameworks:
#     #         #     for o in range(0, NUM_CRITERIA):
#     #         #         Factory.criteria(framework=f)

#     # #         for r in reports:
#     # #             for f in frameworks:
#     # #                 sc = Factory.scorecard(report=r, framework=f, scorer=u)
#     # #                 scorecards.append(sc)
#     # #                 for c in f.criteria:
#     # #                     scorecard_scores.append(
#     # #                         Factory.scorecard_score(scorecard=sc, user=u, criteria=c)
#     # #                     )
#     # #             for s in sources:
#     # #                 r.sources.add(s)
#     # #             r.save()
#     # #         for s in stacks:
#     # #             for r in reports:
#     # #                 s.reports.add(r)
#     # #                 s.save()

#     # #     self.assertEqual(len(reports), NUM_OBJECTS)
#     # #     source_ct = ContentType.objects.get_for_model(Source)

#     # #     start_new = datetime.now()
#     # #     # all_gps = GenericPermission.objects.filter(Q(user=u) | Q(team__in=u.teams) | Q(organization__in=u.organizations)).all().prefetch_related("report", "stack", "framework", "source").values()
#     # #     report_ct = ContentType.objects.get_for_model(Report)
#     # #     report_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=report_ct)
#     # #         & Q(
#     # #             Q(can_score=True)
#     # #             | Q(can_read=True)
#     # #             | Q(can_write=True)
#     # #             | Q(can_administer=True)
#     # #         )
#     # #         & Q(
#     # #             Q(user=u)
#     # #             | Q(team__in=u.teams)
#     # #             | Q(organization__in=u.organizations)
#     # #         )
#     # #     ).all()
#     # #     all_report_gp_ids = report_gps.values_list("object_id", flat=True)
#     # #     all_report_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=report_ct)
#     # #     ).all().values("object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id")

#     # #     all_reports = Report.objects.filter(id__in=all_report_gp_ids).all()

#     # #     source_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=source_ct)
#     # #         & Q(
#     # #             Q(can_score=True)
#     # #             | Q(can_read=True)
#     # #             | Q(can_write=True)
#     # #             | Q(can_administer=True)
#     # #         )
#     # #         & Q(
#     # #             Q(user=u)
#     # #             | Q(team__in=u.teams)
#     # #             | Q(organization__in=u.organizations)
#     # #         )
#     # #     ).all()
#     # #     all_source_gp_ids = source_gps.values_list("object_id", flat=True)
#     # #     all_source_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=source_ct)
#     # #     ).all().values("object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id")

#     # #     all_sources = Source.objects.filter(id__in=all_source_gp_ids)

#     # #     framework_ct = ContentType.objects.get_for_model(Framework)
#     # #     # all_framework_gps = (
#     # #     #     GenericPermission.objects.filter(
#     # #     #         Q(content_type=framework_ct)
#     # #     #         & Q(
#     # #     #             Q(can_score=True)
#     # #     #             | Q(can_read=True)
#     # #     #             | Q(can_write=True)
#     # #     #             | Q(can_administer=True)
#     # #     #         )
#     # #     #         & Q(
#     # #     #             Q(user=u)
#     # #     #             | Q(team__in=u.teams)
#     # #     #             | Q(organization__in=u.organizations)
#     # #     #         )
#     # #     #     )
#     # #     #     .all()
#     # #     #     .values_list("object_id", flat=True)
#     # #     # )
#     # #     framework_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=framework_ct)
#     # #         & Q(
#     # #             Q(can_score=True)
#     # #             | Q(can_read=True)
#     # #             | Q(can_write=True)
#     # #             | Q(can_administer=True)
#     # #         )
#     # #         & Q(
#     # #             Q(user=u)
#     # #             | Q(team__in=u.teams)
#     # #             | Q(organization__in=u.organizations)
#     # #         )
#     # #     ).all()
#     # #     all_framework_gp_ids = framework_gps.values_list("object_id", flat=True)
#     # #     all_framework_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=framework_ct)
#     # #     ).all().values("object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id")

#     # #     all_frameworks = Framework.objects.filter(id__in=all_framework_gp_ids)

#     # #     stack_ct = ContentType.objects.get_for_model(Stack)
#     # #     # all_stack_gps = (
#     # #     #     GenericPermission.objects.filter(
#     # #     #         Q(content_type=stack_ct)
#     # #     #         & Q(
#     # #     #             Q(can_score=True)
#     # #     #             | Q(can_read=True)
#     # #     #             | Q(can_write=True)
#     # #     #             | Q(can_administer=True)
#     # #     #         )
#     # #     #         & Q(
#     # #     #             Q(user=u)
#     # #     #             | Q(team__in=u.teams)
#     # #     #             | Q(organization__in=u.organizations)
#     # #     #         )
#     # #     #     )
#     # #     #     .all()
#     # #     #     .values_list("object_id", flat=True)
#     # #     # )
#     # #     stack_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=stack_ct)
#     # #         & Q(
#     # #             Q(can_score=True)
#     # #             | Q(can_read=True)
#     # #             | Q(can_write=True)
#     # #             | Q(can_administer=True)
#     # #         )
#     # #         & Q(
#     # #             Q(user=u)
#     # #             | Q(team__in=u.teams)
#     # #             | Q(organization__in=u.organizations)
#     # #         )
#     # #     ).all()
#     # #     all_stack_gp_ids = stack_gps.values_list("object_id", flat=True)
#     # #     all_stack_gps = GenericPermission.objects.filter(
#     # #         Q(content_type=stack_ct)
#     # #     ).all().values("object_id", "content_type_id", "can_read", "can_write", "can_score", "can_administer", "user_id", "organization_id", "team_id")

#     # #     all_stacks = Stack.objects.filter(id__in=all_stack_gp_ids)

#     # #     all_scorecards_ids = Scorecard.objects.filter(report_id__in=all_report_gp_ids).values_list("id", flat=True)
#     # #     all_scorecards = Scorecard.objects.filter(report_id__in=all_report_gp_ids).all()
#     # #     all_scorecard_scores = ScorecardScore.objects.filter(scorecard_id__in=all_scorecards_ids).all()

#     # #     all_team_people = (
#     # #         TeamMember.objects.filter(team__in=u.teams)
#     # #         .prefetch_related("user", "team")
#     # #         .values()
#     # #     )
#     # #     all_org_people = (
#     # #         OrganizationRole.objects.filter(organization__in=u.organizations)
#     # #         .prefetch_related("user", "organization")
#     # #         .values()
#     # #     )
#     # #     all_inboxitems = (
#     # #         InboxItem.objects.filter(user=u).prefetch_related("comment").values()
#     # #     )
#     # #     all_subscriptions = ObjectSubscription.objects.filter(user=u).values()
#     # #     all_tags = Tag.objects.filter(Q(user=u)| Q(organization__in=u.organizations)).values()
#     # #     all_tagged_objects = TaggedObject.objects.filter(tag__in=all_tags).values()

#     # #     gps = (
#     # #         GenericPermission.objects.filter(
#     # #             Q(
#     # #                 Q(can_score=True)
#     # #                 | Q(can_read=True)
#     # #                 | Q(can_write=True)
#     # #                 | Q(can_administer=True)
#     # #             )
#     # #             & Q(
#     # #                 Q(user=u)
#     # #                 | Q(team__in=u.teams)
#     # #                 | Q(organization__in=u.organizations)
#     # #             )
#     # #         )
#     # #         .all()
#     # #         .values_list(
#     # #             "object_id",
#     # #             "content_type_id",
#     # #             "can_score",
#     # #             "can_read",
#     # #             "can_write",
#     # #             "can_administer",
#     # #         )
#     # #     )
#     # #     cts = ContentType.objects.all().values("id", "app_label", "model")
#     # #     ct_framework_id = None
#     # #     ct_report_id = None
#     # #     ct_source_id = None
#     # #     ct_stack_id = None
#     # #     for ct in cts:
#     # #         if ct["model"] == "framework":
#     # #             ct_framework_id = ct["id"]
#     # #         if ct["model"] == "report":
#     # #             ct_report_id = ct["id"]
#     # #         if ct["model"] == "source":
#     # #             ct_source_id = ct["id"]
#     # #         if ct["model"] == "stack":
#     # #             ct_stack_id = ct["id"]
#     # #     cts_shortcuts = {
#     # #         "framework": ct_framework_id,
#     # #         "report": ct_report_id,
#     # #         "source": ct_source_id,
#     # #         "stack": ct_stack_id,
#     # #     }


#     # #     all_subscription_users = ObjectSubscription.objects.filter(
#     # #         Q(object_id__in=all_framework_gp_ids, content_type_id=ct_framework_id) |
#     # #         Q(object_id__in=all_report_gp_ids, content_type_id=ct_report_id) |
#     # #         Q(object_id__in=all_source_gp_ids, content_type_id=ct_source_id) |
#     # #         Q(object_id__in=all_stack_gp_ids, content_type_id=ct_stack_id)
#     # #     ).values_list('user_id', "object_id", "content_type_id")

#     # #     all_comments = Comment.objects.filter(
#     # #         Q(object_id__in=all_framework_gp_ids, content_type_id=ct_framework_id) |
#     # #         Q(object_id__in=all_report_gp_ids, content_type_id=ct_report_id) |
#     # #         Q(object_id__in=all_source_gp_ids, content_type_id=ct_source_id) |
#     # #         Q(object_id__in=all_stack_gp_ids, content_type_id=ct_stack_id)
#     # #     ).values('user_id', "object_id", "content_type_id", "body", "edited")

#     # #     # all_{ct_name}_gps
#     # #     users_i_know_about_ids = []
#     # #     for gp in all_report_gps:
#     # #         if gp["user_id"]:
#     # #             users_i_know_about_ids.append(gp["user_id"])
#     # #     for gp in all_framework_gps:
#     # #         if gp["user_id"]:
#     # #             users_i_know_about_ids.append(gp["user_id"])
#     # #     for gp in all_source_gps:
#     # #         if gp["user_id"]:
#     # #             users_i_know_about_ids.append(gp["user_id"])
#     # #     for gp in all_stack_gps:
#     # #         if gp["user_id"]:
#     # #             users_i_know_about_ids.append(gp["user_id"])
#     # #     users_i_know_about = User.objects.filter(id__in=users_i_know_about_ids).all()

#     # #     users_i_know_about_by_id = {}
#     # #     users_i_know_about_by_ox_id = {}
#     # #     for user in users_i_know_about:
#     # #         users_i_know_about_by_id[f"{u.id}"] = user.to_data(u)
#     # #         users_i_know_about_by_ox_id[f"{u.ox_id}"] = user.to_data(u)

#     # #     all_objs_legacy_js = []
#     # #     all_user_objs = {
#     # #         "user": u,
#     # #         "reports": [],
#     # #         "frameworks": [],
#     # #         "sources": [],
#     # #         "stacks": [],
#     # #         "inboxitems": [],
#     # #         "teams": [],
#     # #         "tags": [],
#     # #         "comments": all_comments,
#     # #         "tagged_objects": all_tagged_objects,
#     # #         "organizations": [],
#     # #         "all_gps": gps,
#     # #         "all_report_gp_ids": all_report_gp_ids,
#     # #         "all_report_gps": all_report_gps,
#     # #         "all_framework_gp_ids": all_framework_gp_ids,
#     # #         "all_framework_gps": all_framework_gps,
#     # #         "all_source_gp_ids": all_source_gp_ids,
#     # #         "all_source_gps": all_source_gps,
#     # #         "all_stack_gp_ids": all_stack_gp_ids,
#     # #         "all_stack_gps": all_stack_gps,
#     # #         "all_scorecard_scores": all_scorecard_scores,
#     # #         "content_types": cts,
#     # #         "cts_shortcuts": cts_shortcuts,
#     # #         "subscriptions": all_subscriptions,
#     # #         "all_subscription_users": all_subscription_users,
#     # #         "users_by_id": users_i_know_about_by_id,
#     # #     }
#     # #     for obj in all_reports:
#     # #         all_user_objs["reports"].append(obj)
#     # #         all_objs_legacy_js.append(obj)

#     # #     for obj in all_frameworks:
#     # #         all_user_objs["frameworks"].append(obj)
#     # #         all_objs_legacy_js.append(obj)

#     # #     for obj in all_sources:
#     # #         all_user_objs["sources"].append(obj)
#     # #         all_objs_legacy_js.append(obj)

#     # #     for obj in all_stacks:
#     # #         all_user_objs["stacks"].append(obj)
#     # #         all_objs_legacy_js.append(obj)

#     # #     for obj in all_inboxitems:
#     # #         all_user_objs["inboxitems"].append(obj)
#     # #         all_objs_legacy_js.append(obj)

#     # #     for obj in all_team_people:
#     # #         all_user_objs["teams"].append(obj)
#     # #         all_objs_legacy_js.append(obj)

#     # #     for obj in all_org_people:
#     # #         all_user_objs["organizations"].append(obj)
#     # #         all_objs_legacy_js.append(obj)

#     # #     for obj in all_tags:
#     # #         all_user_objs["tags"].append(obj)
#     # #         all_objs_legacy_js.append(obj)


#     # #     # "subscribers": [rel_by_id(u, "ox_id") for u in s["subscribers"]],

#     # #     # generate_js_data(all_user_objs, requesting_user=u)
#     # #     all_user_output_data = {
#     # #         "user": u.to_data(u),
#     # #         "reports": [obj.to_data_from_precache(u, all_user_objs) for obj in all_reports],
#     # #         # "frameworks": [obj.to_data_from_precache(u, all_user_objs) for obj in all_sources],
#     # #         # "sources": [obj.to_data_from_precache(u, all_user_objs) for obj in all_frameworks],
#     # #         # "stacks": [obj.to_data_from_precache(u, all_user_objs) for obj in all_stacks],
#     # #         # "inboxitems": [obj.to_data_from_precache(u, all_user_objs) for obj in all_inboxitems],
#     # #         # "tags": [obj.to_data_from_precache(u, all_user_objs) for obj in all_tags],
#     # #         # "comments": [obj.to_data_from_precache(u, all_user_objs) for obj in all_comments],
#     # #         # "users": [obj.to_data_from_precache(u, all_user_objs) for obj in users_i_know_about],
#     # #         # "organizations": [obj.to_data_from_precache(u, all_user_objs) for obj in u.organizations],
#     # #         # "teams": [obj.to_data_from_precache(u, all_user_objs) for obj in u.teams],
#     # #         # "subscriptions": [],
#     # #         "scorecards": [sc.to_data_from_precache(u, all_user_objs) for sc in all_scorecards],
#     # #         "scorecardscores": [scs.to_data_from_precache(u, all_user_objs) for scs in all_scorecard_scores],
#     # #         "users": users_i_know_about_by_ox_id,
#     # #     }

#     # #     # for r in all_reports:
#     # #     #     all_user_output_data["reports"].append(r.to_data(u))
#     # #     # for s in all_sources:
#     # #     #     all_user_output_data["sources"].append(s.to_data(u))

#     # #     # for s in all_frameworks:
#     # #     #     all_user_output_data["frameworks"].append(f.to_data(u))
#     # #     # for s in all_stacks:
#     # #     #     all_user_output_data["stacks"].append(s.to_data(u))

#     # #     # pprint.pprint([Source.values_dict_to_data(s, u, all_user_objs) for s in all_sources])
#     # #     end_new = datetime.now()
#     # #     pprint.pprint(all_user_output_data)
#     # #     print(f"Middle time: {1000* (end_new - start_new).total_seconds()} ms\n\n")

#     # def test_legacy_speeds(self):
#     #     users = create_objs(self.user, "user", NUM_OBJECTS, skip_permissions=True)
#     #     teams = []
#     #     organizations = []
#     #     for i in range(0, NUM_OBJECTS):
#     #         o = Factory.organization()
#     #         t = Factory.team(organization=o)
#     #         teams.append(t)
#     #         organizations.append(o)
#     #     for u in users:
#     #         for t in teams:
#     #             t.add_user(u)
#     #             t.save()
#     #         for o in organizations:
#     #             o.add_user(u)
#     #             o.save()
#     #         frameworks = create_objs(u, "framework", NUM_OBJECTS)
#     #         reports = create_objs(u, "report", NUM_OBJECTS)
#     #         sources = create_objs(u, "source", NUM_OBJECTS)
#     #         stacks = create_objs(u, "stack", NUM_OBJECTS)
#     #         scorecards = []
#     #         scorecard_scores = []
#     #         for f in frameworks:
#     #             for o in range(0, NUM_CRITERIA):
#     #                 Factory.criteria(framework=f)

#     #         for r in reports:
#     #             for f in frameworks:
#     #                 sc = Factory.scorecard(report=r, framework=f, scorer=u)
#     #                 scorecards.append(sc)
#     #                 for c in f.criteria:
#     #                     scorecard_scores.append(
#     #                         Factory.scorecard_score(scorecard=sc, user=u, criteria=c)
#     #                     )
#     #             for s in sources:
#     #                 r.sources.add(s)
#     #             r.save()
#     #         for s in stacks:
#     #             for r in reports:
#     #                 s.reports.add(r)
#     #                 s.save()

#     #     self.assertEqual(len(reports), NUM_OBJECTS)
#     #     request = mock.Mock()
#     #     request.user = u

#     #     start = datetime.now()
#     #     context = get_context(request)
#     #     # pprint.pprint(context)
#     #     end = datetime.now()
#     #     print(f"Legacy time: {1000 * (end - start).total_seconds()} ms\n\n")

# # fmt: on
