from api.events.base import BaseEventHandler
from collaboration.models import ObjectSubscription
from frameworks.models import Framework, Criteria
from organizations.models import GenericPermission
from reports.models import Report
from django.contrib.contenttypes.models import ContentType


class CreateFrameworkHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.process_tags = True
        self.handle_pseudoteam(data)
        if self.specified_permissions:
            del data["pseudoteam"]

        f = Framework.authorized_objects.authorize(user=request.user).create(**data)
        f.created_by = request.user
        f.modified_by = request.user
        f.save()
        self.add_pseudoteam_permissions(f, request, created=True)
        obj_list = [
            f,
        ]

        # Subscribe the creator to this object.
        ct = ContentType.objects.get_for_model(f)
        ObjectSubscription.objects.get_or_create(
            object_id=f.pk, content_type=ct, user=request.user
        )
        self.tagged_obj = f
        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": f,
        }


class UpdateFrameworkHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # TODO: this could use a LOT of optimization.

        # Return all objects created or modified, and success true or false.
        obj_list = []
        self.process_tags = True
        self.handle_pseudoteam(data)
        if self.specified_permissions:
            del data["pseudoteam"]
        f = Framework.authorized_objects.authorize(user=request.user).writeable.get(
            ox_id=data["id"]
        )

        # If "criteria" is passed in, it's treated as the complete list of criteria
        # e.g. delete any criteria that aren't in the list, update any with id
        # and if there is no id, treat it as new.

        criteria = None
        if "criteria" in data:
            criteria = data["criteria"]
            del data["criteria"]
        updated_framework = False
        updated_criteria = False
        for k, v in data.items():
            if k in Framework.api_writable_fields:
                if getattr(f, k) != v:
                    setattr(f, k, v)
                    updated_framework = True
        if updated_framework:
            f.modified_by = request.user
            f.save()

        current_criteria_ids = []
        previous_criteria_ids = []
        if criteria is not None:
            updated_criteria = True
            previous_criteria_ids = f.criteria.values_list("id", flat=True)
            index = 0
            updated_ox_ids = []
            for c in criteria:
                if "id" in c:
                    updated_ox_ids.append(c["id"])

            print(updated_ox_ids)
            if f.criteria.count() > 0:
                previous_indexes = [
                    i
                    for i in f.criteria.exclude(index=None)
                    .filter(ox_id__in=updated_ox_ids)
                    .values_list("index", flat=True)
                ]
                if len(previous_indexes) > 0:
                    index = max(previous_indexes) + 1

            for c_data in criteria:
                found = False
                if "id" in c_data:
                    try:
                        c = f.criteria.get(ox_id=c_data["id"])
                        found = True
                        del c_data["id"]
                    except Criteria.DoesNotExist:
                        pass
                if not found:
                    c = Criteria.objects.create(framework=f)
                    updated_criteria = True
                for k, v in c_data.items():
                    if k in Criteria.api_writable_fields:
                        setattr(c, k, v)
                        updated_criteria = True

                if c.index is None:
                    c.index = index
                    index += 1
                c.save()
                current_criteria_ids.append(c.pk)

            # Delete criteria that were omitted.
            if len(current_criteria_ids) == 0:
                f.criteria_set.all().delete()
                updated_criteria = True
            else:
                for p_id in previous_criteria_ids:
                    if p_id not in current_criteria_ids:
                        c = f.criteria.get(pk=p_id)
                        c.delete()
                        updated_criteria = True

        if self.specified_permissions:
            self.add_pseudoteam_permissions(f, request)
            updated_framework = True
        # TODO when we want history changes, uncomment this.
        # f.generate_history_change(request.user, "update_framework")

        if updated_framework or updated_criteria:
            f.save()

        if updated_criteria:
            for c in f.criteria:
                c = Criteria.objects.get(pk=c.pk)

        if updated_framework or updated_criteria:
            for sc in f.scorecards:
                for c in f.criteria:
                    sc.scorecardscore_set.get_or_create(criteria=c)
                for p_id in previous_criteria_ids:
                    if p_id not in current_criteria_ids:
                        sc.scorecardscore_set.filter(criteria__id=p_id).delete()

        # f will automatically also return the criteria.
        self.tagged_obj = f
        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": f,
        }


class DeleteFrameworkHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        f = Framework.authorized_objects.authorize(user=request.user).administered.get(
            ox_id=data["id"]
        )
        self.process_tags = False
        if "tags" in data:
            del data["tags"]
        self.tags = []
        self.handle_tags(f)

        f.delete()
        self.tags = None

        reports = []

        return {
            "obj_list": reports,
            "success": True,
            "target_obj": None,
            "deleted": [
                {"type": "frameworks", "pk": data["id"]},
            ],
        }


class GetFrameworkHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        f = Framework.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["id"]
        )
        return {
            "obj_list": [
                f,
            ],
            "success": True,
            "target_obj": f,
        }


class GetFrameworksHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        f = Framework.authorized_objects.authorize(user=request.user).findable.filter(
            **data
        )
        return {
            "obj_list": f.all(),
            "success": True,
            "target_obj": None,
        }


class CloneFrameworkHandler(BaseEventHandler):
    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        self.handle_pseudoteam(data)
        if self.specified_permissions:
            del data["pseudoteam"]
        f = Framework.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=data["id"]
        )
        # Clone framework
        if "name" in data:
            name = data["name"]
        else:
            name = f.name
        if "subtitle" in data:
            subtitle = data["subtitle"]
        else:
            subtitle = f.subtitle

        f2 = Framework.objects.create(
            name=name,
            subtitle=subtitle,
            created_by=request.user,
            modified_by=request.user,
            parent=f,
        )

        # Clone criteria
        for c in f.criteria:
            Criteria.objects.create(
                framework=f2,
                name=c.name,
                description=c.description,
                weight=c.weight,
                index=c.index,
                created_by=request.user,
                modified_by=request.user,
            )

        ct = ContentType.objects.get_for_model(Framework)

        # Clone permissions
        # for gp in GenericPermission.objects.filter(
        #     content_type=ct,
        #     object_id=f.pk,
        # ):
        #     GenericPermission.objects.create(
        #         content_type=ct,
        #         object_id=f2.pk,
        #         user=gp.user,
        #         team=gp.team,
        #         organization=gp.organization,
        #         can_read=gp.can_read,
        #         can_write=gp.can_write,
        #         can_administer=gp.can_administer,
        #     )
        # self.add_pseudoteam_permissions(f2, request, created=True)

        # If we instead want to let users take content private:
        # gp =
        GenericPermission.objects.create(
            content_type=ct,
            object_id=f2.pk,
            user=request.user,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=True,
        )
        # print(gp)

        f2 = Framework.objects.get(pk=f2.pk)
        obj_list = [
            f2,
        ]

        return {
            "obj_list": obj_list,
            "success": True,
            "target_obj": f2,
        }
