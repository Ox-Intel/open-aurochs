import datetime
import jwt
import json
from django.apps import apps
from django.contrib.admin.utils import NestedObjects
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from utils.encryption import create_unique_ox_id
from utils.helpers import rel, REL_SPLIT_START, REL_SPLIT_END
from django.utils.functional import cached_property
from simple_history.models import HistoricalRecords

SEMICOLON_ESCAPE_SEQUENCE = "!!!~~~Semicolon Escape~~~###"
CACHE_KEY_DELIMITER = "/;|;/"


class DataDictMixin(object):
    def all_of_type_in_user_objects(self, related_type, related_field, user_data):
        related = []
        for o in user_data[related_type]:
            # print(o[related_field])
            if self in o[related_field]:
                related.append(o)
        return o

    @cached_property
    def created_at_ms(self):
        if self.created_at:
            return self.created_at.timestamp() * 1000
        return None

    @cached_property
    def modified_at_ms(self):
        if self.modified_at:
            return self.modified_at.timestamp() * 1000
        return self.created_at_ms

    def save(self, *args, **kwargs):
        super(DataDictMixin, self).save(*args, **kwargs)

    def cache_key_from_class_and_pk(self, cls, pk):
        return f"to_js_data-{cls.__name__}-{pk}"

    @cached_property
    def instance_cache_key_cache_key(self):
        return f"cache-key-list-{self.__class__.__name__}-{self.ox_id}"

    def add_to_instance_cache_key_list(self, new_key):
        # print("adding %s to cache key list for %s" % (new_key, self))
        if new_key:
            key_list = self.instance_cache_key_list
            if new_key not in key_list:
                key_list.append(new_key)
                cache.set(
                    self.instance_cache_key_cache_key,
                    CACHE_KEY_DELIMITER.join(key_list),
                )

    @property
    def instance_cache_key_list(self):
        l = cache.get(self.instance_cache_key_cache_key, None)
        if l:
            return l.split(CACHE_KEY_DELIMITER)
        return []

    def cache_key(self, requesting_user):
        if (
            hasattr(self, "user_specific_caching")
            and self.user_specific_caching
            and requesting_user
        ):
            return f"-ox-{self.__class__.__name__}-{self.pk}-{requesting_user.ox_id}"
        return f"-ox-{self.__class__.__name__}-{self.pk}"

    @cached_property
    def permissions_dict(self):
        _, p_dict = self.get_permissions_obj()
        return p_dict

    def get_permissions_obj(self):
        related_objects = []
        p = self.permissions
        val = {
            "score": {"teams": [], "organizations": [], "users": []},
            "read": {"teams": [], "organizations": [], "users": []},
            "write": {"teams": [], "organizations": [], "users": []},
            "administer": {"teams": [], "organizations": [], "users": []},
        }
        for o in p["score"]["teams"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["score"]["teams"].append(rel(o))
        for o in p["read"]["teams"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["read"]["teams"].append(rel(o))
        for o in p["write"]["teams"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["write"]["teams"].append(rel(o))
        for o in p["administer"]["teams"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["administer"]["teams"].append(rel(o))
        for o in p["score"]["organizations"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["score"]["organizations"].append(rel(o))
        for o in p["read"]["organizations"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["read"]["organizations"].append(rel(o))
        for o in p["write"]["organizations"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["write"]["organizations"].append(rel(o))
        for o in p["administer"]["organizations"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["administer"]["organizations"].append(rel(o))
        for o in p["score"]["users"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["score"]["users"].append(rel(o))
        for o in p["read"]["users"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["read"]["users"].append(rel(o))
        for o in p["write"]["users"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["write"]["users"].append(rel(o))
        for o in p["administer"]["users"]:
            if not hasattr(o, "deleted") or not o.deleted:
                related_objects.append(o)
                val["administer"]["users"].append(rel(o))
        return related_objects, val


class SoftDeletionQuerySet(models.query.QuerySet):
    def delete(self):
        super(SoftDeletionQuerySet, self).update(
            deleted=True, deleted_at=timezone.now()
        )
        for o in self.all():
            nested_object = NestedObjects("default")
            nested_object.collect([o])
            self._delete_nested(nested_object.nested())

    def _delete_nested(self, obj):
        try:
            for o in obj:
                self._delete_nested(o)
        except TypeError:
            if obj is not self:
                obj.delete()

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.include_deleted = kwargs.pop("include_deleted", False)
        super(BaseManager, self).__init__(*args, **kwargs)

    def _delete_nested(self, obj):
        try:
            for o in obj:
                self._delete_nested(o)
        except TypeError:
            if obj is not self:
                obj.delete()

    def delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
        nested_object = NestedObjects("default")
        nested_object.collect([self])
        self._delete_nested(nested_object.nested())

    def get_queryset(self):
        if self.include_deleted:
            return SoftDeletionQuerySet(self.model).all()
        return SoftDeletionQuerySet(self.model).filter(deleted=False)


class AuthorizedManager(BaseManager):
    def authorize(self, **kwargs):
        if "user" in kwargs or "team" in kwargs or "organization" in kwargs:
            self._auth_kwargs = kwargs
        return self

    def deauthorize(self, **kwargs):
        self._auth_kwargs = None
        return self

    def get_queryset(self):
        if not hasattr(self, "_auth_kwargs") or not self._auth_kwargs:
            raise PermissionDenied(
                "Tried to call authorized query without first calling .authorize()"
            )
        if self.include_deleted:
            return self.findable.all()
        return self.findable.exclude(deleted=True)

    def create(self, *args, **kwargs):
        from organizations.models import GenericPermission

        if not hasattr(self, "_auth_kwargs") or not self._auth_kwargs:
            raise PermissionDenied(
                "Tried to call create without first calling .authorize()"
            )

        if "user" not in self._auth_kwargs or not self._auth_kwargs["user"]:
            raise PermissionDenied(
                "Tried to call create without specifying a user in .authorize()"
            )

        kwargs["created_by"] = self._auth_kwargs["user"]
        kwargs["modified_by"] = self._auth_kwargs["user"]
        ret = super(AuthorizedManager, self).create(*args, **kwargs)
        gp, _ = GenericPermission.objects.get_or_create(
            user=kwargs["created_by"],
            content_type=ContentType.objects.get_for_model(ret),
            object_id=ret.pk,
        )
        gp.can_score = True
        gp.can_read = True
        gp.can_write = True
        gp.can_administer = True
        gp.save()
        cache.delete(
            f"permission-pk-score-{ret.__class__.__name__}-user-{self._auth_kwargs['user'].ox_id}"
        )
        cache.delete(
            f"permission-pk-read-{ret.__class__.__name__}-user-{self._auth_kwargs['user'].ox_id}"
        )
        cache.delete(
            f"permission-pk-write-{ret.__class__.__name__}-user-{self._auth_kwargs['user'].ox_id}"
        )
        cache.delete(
            f"permission-pk-administer-{ret.__class__.__name__}-user-{self._auth_kwargs['user'].ox_id}"
        )
        return ret

    # objects.readable(user=user)
    # objects.can_read(user=user)
    # objects.get_readable(user=user)
    # objects.has_read_permission(user=user)
    # authorized_objects(user=user).readable()
    # authorized_objects(user=user).can_read()
    # authorized_objects.authorize(user=user).readable
    # authorized_objects.authorize(user=user).writeable
    # authorized_objects.authorize(user=user).administered

    def get_cached_permission_pks(
        self, permission_name, user=None, team=None, organization=None
    ):
        user_pks = []
        team_pks = []
        organization_pks = []

        if self.model:
            # Disables caching for now, it's plenty fast with the serializer.
            if user:
                # user_cache_key = f"permission-pk-{permission_name}-{self.model.__name__}-user-{user.ox_id}"
                # user_pks = cache.get(user_cache_key, None)
                # if user_pks is None:
                user_pks = self.get_gfk_permission(permission_name, user=user)
                # user.add_to_instance_cache_key_list(user_cache_key)
                # cache.set(user_cache_key, user_pks)
            if team:
                # team_cache_key = f"permission-pk-{permission_name}-{self.model.__name__}-team-{team.pk}"
                # team_pks = cache.get(team_cache_key, None)
                # if team_pks is None:
                team_pks = self.get_gfk_permission(permission_name, team=team)
                # team.add_to_instance_cache_key_list(team_cache_key)
                # cache.set(team_cache_key, team_pks)
            if organization:
                # organization_cache_key = f"permission-pk-{permission_name}-{self.model.__name__}-organization-{organization.pk}"
                # organization_pks = cache.get(organization_cache_key, None)
                # if organization_pks is None:
                organization_pks = self.get_gfk_permission(
                    permission_name, organization=organization
                )
                # organization.add_to_instance_cache_key_list(organization_cache_key)
                # cache.set(organization_cache_key, organization_pks)

        all_pks = set(user_pks + team_pks + organization_pks)
        return all_pks

    def get_cached_permission_qs(
        self, permission_name, user=None, team=None, organization=None
    ):
        if not user and not team and not organization:
            return SoftDeletionQuerySet(self.model).none()
        qs = SoftDeletionQuerySet(self.model)

        return qs.filter(
            pk__in=self.get_cached_permission_pks(
                permission_name, user, team, organization
            )
        ).exclude(deleted=True)

    @property
    def findable(self):
        user = self._auth_kwargs.get("user", None)
        team = self._auth_kwargs.get("team", None)
        organization = self._auth_kwargs.get("organization", None)

        if not user and not team and not organization:
            return SoftDeletionQuerySet(self.model).none()
        qs = SoftDeletionQuerySet(self.model)

        pks = list(
            set().union(
                self.scoreable_pks,
                self.readable_pks,
                # this is possible to do with just score and read,
                # since you can't have edit or admin without them
                # but we haven't migrated the data and I don't
                # totally trust it. -S
                self.writeable_pks,
                self.administered_pks,
            )
        )

        return qs.filter(pk__in=pks).exclude(deleted=True)

    @property
    def scoreable(self):
        return self.get_cached_permission_qs("score", **self._auth_kwargs)
        # return self.get_gfk_permission("read", **self._auth_kwargs)

    @property
    def readable(self):
        return self.get_cached_permission_qs("read", **self._auth_kwargs)
        # return self.get_gfk_permission("read", **self._auth_kwargs)

    @property
    def writeable(self):
        return self.get_cached_permission_qs("write", **self._auth_kwargs)

    @property
    def administered(self):
        return self.get_cached_permission_qs("administer", **self._auth_kwargs)

    @property
    def scoreable_pks(self):
        return self.get_cached_permission_pks("score", **self._auth_kwargs)
        # return self.get_gfk_permission("read", **self._auth_kwargs)

    @property
    def readable_pks(self):
        return self.get_cached_permission_pks("read", **self._auth_kwargs)
        # return self.get_gfk_permission("read", **self._auth_kwargs)

    @property
    def writeable_pks(self):
        return self.get_cached_permission_pks("write", **self._auth_kwargs)

    @property
    def administered_pks(self):
        return self.get_cached_permission_pks("administer", **self._auth_kwargs)

    def get_gfk_permission(
        self, permission_name, pk=None, user=None, team=None, organization=None
    ):
        from organizations.models import GenericPermission

        gp_qs_user = []
        gp_qs_team = []
        gp_qs_org = []
        permissions = {f"can_{permission_name}": True}
        if pk:
            permissions["object_id"] = pk
        if user:
            gp_qs_user = list(
                GenericPermission.objects.filter(
                    user=user,
                    content_type=ContentType.objects.get_for_model(self.model),
                    **permissions,
                )
                .distinct()
                .values_list("object_id", flat=True)
            )
            if user.teams:
                for t in user.teams:
                    gp_qs_user += list(
                        GenericPermission.objects.filter(
                            team=t,
                            content_type=ContentType.objects.get_for_model(self.model),
                            **permissions,
                        )
                        .distinct()
                        .values_list("object_id", flat=True)
                    )
            if user.organizations:
                for o in user.organizations:
                    gp_qs_user += list(
                        GenericPermission.objects.filter(
                            organization=o,
                            content_type=ContentType.objects.get_for_model(self.model),
                            **permissions,
                        )
                        .distinct()
                        .values_list("object_id", flat=True)
                    )
        if team:
            gp_qs_team = list(
                GenericPermission.objects.filter(
                    team=team,
                    content_type=ContentType.objects.get_for_model(self.model),
                    **permissions,
                )
                .distinct()
                .values_list("object_id", flat=True)
            )
        if organization:
            gp_qs_org = list(
                GenericPermission.objects.filter(
                    organization=organization,
                    content_type=ContentType.objects.get_for_model(self.model),
                    **permissions,
                )
                .distinct()
                .values_list("object_id", flat=True)
            )
        gp_pks = list(set(gp_qs_user + gp_qs_team + gp_qs_org))
        return gp_pks


class BaseModel(DataDictMixin, models.Model):
    objects = BaseManager(include_deleted=False)
    objects_with_deleted = BaseManager(include_deleted=True)
    created_at = models.DateTimeField(
        db_index=True, blank=True, null=True, default=timezone.now
    )
    modified_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    # TODO: Legacy fields from Service codebase, should be moved to history logs/version in a future data migration
    created_by = models.ForeignKey(
        "organizations.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created_by",
    )
    modified_by = models.ForeignKey(
        "organizations.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_modified_by",
    )
    deleted = models.BooleanField(null=True, default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    history = HistoricalRecords(inherit=True)

    @property
    def create_date(self):
        return self.created_at

    @create_date.setter
    def create_date(self, value):
        self.created_at = value

    @property
    def last_modified(self):
        return self.modified_at

    @last_modified.setter
    def last_modified(self, value):
        self.modified_at = value

    def _delete_nested(self, obj):
        try:
            for o in obj:
                self._delete_nested(o)
        except TypeError:
            if obj is not self:
                obj.delete()

    def delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
        nested_object = NestedObjects("default")
        nested_object.collect([self])
        self._delete_nested(nested_object.nested())

    def cache_invalidate_accessors_and_delete_permissions(self):
        from organizations.models import GenericPermission

        ct = ContentType.objects.get_for_model(self)
        for gp in GenericPermission.objects.filter(
            object_id=self.pk, content_type=ct
        ).all():
            gp.delete()

    class Meta:
        abstract = True


class TaggableModel(object):
    def tags(self, requesting_user):
        return self.get_tags_for_user(requesting_user)

    def get_tags_for_user(self, requesting_user):
        from organizations.models import TaggedObject

        ct = ContentType.objects.get_for_model(self)
        qs_filter = None
        qs_filter = Q(
            object_id=self.pk,
            content_type=ct,
            tag__user=requesting_user,
        )
        for o in requesting_user.organizations:
            if not qs_filter:
                qs_filter = Q(
                    object_id=self.pk,
                    content_type=ct,
                    tag__organization=o,
                )
            else:
                qs_filter |= Q(
                    object_id=self.pk,
                    content_type=ct,
                    tag__organization=o,
                )
        if qs_filter:
            return [d.tag for d in TaggedObject.objects.filter(qs_filter).distinct()]
        return []

    def search_text(self, requesting_user):
        text = f"{self.__class__.__name__.lower()}:{self.pk}"
        if self.name:
            text += "|name:" + self.name
        for t in self.tags(requesting_user):
            if t.name:
                text += "|tag:" + t.name

        if hasattr(self, "stacks"):
            for s in self.stacks(requesting_user):
                if s.name:
                    text += "|instk:" + s.name
        if text != "":
            return text + "|"
        return text

    def get_tags_for_org(self, organization):
        from organizations.models import TaggedObject

        ct = ContentType.objects.get_for_model(self)
        return TaggedObject.objects.filter(
            object_id=self.pk,
            content_type=ct,
            tag__organization=organization,
        ).values("tag")

    def set_tags(self, tag_list, requesting_user=None):
        from organizations.models import TaggedObject, Tag, GenericPermission

        # print("set_tags")
        # print(self)
        # print(self.__dict__)
        # print(tag_list)

        # tag_list is a list like:
        # [
        #     {
        #         "id": 4,
        #     },
        #     {
        #         "name": "New tag"
        #     }
        # ]
        ct = ContentType.objects.get_for_model(self)
        object_orgs = []
        object_teams = []

        for gp in GenericPermission.objects.filter(
            content_type=ct, object_id=self.pk
        ).filter(
            Q(can_score=True)
            | Q(can_read=True)
            | Q(can_write=True)
            | Q(can_administer=True)
        ):
            if gp.organization and gp.organization not in object_orgs:
                if gp.organization.is_member(requesting_user):
                    object_orgs.append(gp.organization)
            if gp.team and gp.team not in object_teams:
                if gp.team.is_member(requesting_user):
                    object_teams.append(gp.team)
                    if gp.team.organization not in object_orgs:
                        object_orgs.append(gp.team.organization)

        valid_tos = []
        valid_tags = []
        deleted_tags = []

        # Add all new tags
        # print("tag_list")
        # print(tag_list)
        for tag in tag_list:
            if len(tag["name"]) > 0:
                if len(object_orgs) > 0:
                    for o in object_orgs:
                        t, _ = Tag.objects.get_or_create(
                            name=tag["name"], organization=o
                        )
                        to, _ = TaggedObject.objects.get_or_create(
                            tag=t,
                            object_id=self.pk,
                            content_type=ct,
                        )
                        valid_tos.append(to.pk)
                        valid_tags.append(t)
                elif requesting_user:
                    t, _ = Tag.objects.get_or_create(
                        name=tag["name"], user=requesting_user
                    )
                    to, _ = TaggedObject.objects.get_or_create(
                        tag=t,
                        object_id=self.pk,
                        content_type=ct,
                    )
                    valid_tos.append(to.pk)
                    valid_tags.append(t)

        potentially_stale_tags = []

        # Remove all tags not listed.
        for o in object_orgs:
            for to in (
                TaggedObject.objects.filter(
                    Q(
                        object_id=self.pk,
                        content_type=ct,
                        tag__organization=o,
                    )
                )
                .exclude(pk__in=valid_tos)
                .distinct()
            ):
                # if to.ox_id not in valid_tos:
                # print("stale: ")
                # print(to)

                # ensure that this to is not one that this user simply can't know about.
                potentially_stale_tags.append(to.tag)
                to.delete()

        if requesting_user:
            for to in (
                TaggedObject.objects.filter(
                    object_id=self.pk,
                    content_type=ct,
                    tag__user=requesting_user,
                )
                .exclude(pk__in=valid_tos)
                .distinct()
            ):
                # if to.ox_id not in valid_tos:
                # print("stale: ")
                # print(to)
                potentially_stale_tags.append(to.tag)
                to.delete()

        # Delete tags that aren't tagging anything.
        # print("len(valid_tos) %s" % len(valid_tos))
        # print(valid_tos)
        # print(potentially_stale_tags)
        if len(valid_tos) == 0 and tag_list is not None:
            # Remove all tags.
            for o in object_orgs:
                for to in TaggedObject.objects.filter(
                    object_id=self.pk,
                    content_type=ct,
                    tag__organization=o,
                ).all():
                    potentially_stale_tags.append(to.tag)
                    to.delete()
            for to in TaggedObject.objects.filter(
                object_id=self.pk,
                content_type=ct,
                tag__user=requesting_user,
            ).all():
                potentially_stale_tags.append(to.tag)
                to.delete()

        for tag in potentially_stale_tags:
            if tag.taggedobject_set.exclude(deleted=True).count() == 0:
                deleted_tags.append(tag.pk)
                tag.delete()

        return valid_tags, deleted_tags


class SubscribableMixin(object):
    def subscribed(self, requesting_user):
        from collaboration.models import ObjectSubscription

        ct = ContentType.objects.get_for_model(self)
        return (
            ObjectSubscription.objects.filter(
                object_id=self.pk, user=requesting_user, content_type=ct
            ).count()
            > 0
        )

    def generate_history_change(self, requesting_user, change_type, description=None):
        from history.models import ObjectHistoryChange

        ct = ContentType.objects.get_for_model(self)
        ObjectHistoryChange.objects.create(
            change_type=change_type,
            description=description,
            created_by=requesting_user,
            changed_by_id=requesting_user.ox_id,
            changed_by_name=requesting_user.full_name,
            content_type=ct,
            object_id=self.pk,
        )


class CommentMixin(object):
    @cached_property
    def comments(self):
        from collaboration.models import Comment

        ct = ContentType.objects.get_for_model(self)
        return (
            Comment.objects.filter(object_id=self.pk, content_type=ct, deleted=False)
            .order_by("created_at")
            .all()
        )

    @cached_property
    def subscribers(self):
        from collaboration.models import ObjectSubscription

        ct = ContentType.objects.get_for_model(self)
        return [
            os.user
            for os in ObjectSubscription.objects.filter(
                object_id=self.pk, content_type=ct, deleted=False
            )
            .order_by("created_at")
            .all()
        ]


class PermissionedModel(CommentMixin, SubscribableMixin, TaggableModel, BaseModel):
    # This *happens* to be the subscribeable and taggable and commentable models.  Split this out and refactor when that changes!
    user_specific_lookups = [
        "tags",
        "subscribed",
    ]
    objects = BaseManager(include_deleted=False)
    objects_with_deleted = BaseManager(include_deleted=True)
    raw_objects = models.Manager()
    authorized_objects = AuthorizedManager()

    def can_permission(self, permission_name, **kwargs):
        if (
            "user" not in kwargs
            and "team" not in kwargs
            and "organization" not in kwargs
        ):
            raise PermissionDenied(
                f"Check for {permission_name} called without user, team, or organization keyword argument."
            )
        else:
            key = ""
            if "user" in kwargs:
                key += f"_user_{kwargs['user'].ox_id}_{permission_name}"
            if "team" in kwargs:
                key += f"_team_{kwargs['team'].ox_id}_{permission_name}"
            if "organization" in kwargs:
                key += f"_organization_{kwargs['organization'].ox_id}_{permission_name}"
        if not hasattr(self, key):
            if self.pk in self.__class__.authorized_objects.get_gfk_permission(
                permission_name, pk=self.pk, **kwargs
            ):
                setattr(self, key, True)
            else:
                setattr(self, key, False)
        return getattr(self, key)

    def can_score(self, **kwargs):
        return self.can_permission("score", **kwargs)

    def can_read(self, **kwargs):
        return self.can_permission("read", **kwargs)

    def can_write(self, **kwargs):
        return self.can_permission("write", **kwargs)

    def can_administer(self, **kwargs):
        return self.can_permission("administer", **kwargs)

    def can_know_exists(self, **kwargs):
        return (
            self.can_score(**kwargs)
            or self.can_read(**kwargs)
            or self.can_write(**kwargs)
            or self.can_administer(**kwargs)
        )

    def set_permission(
        self,
        acting_user=None,
        user=None,
        team=None,
        organization=None,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    ):
        from organizations.models import GenericPermission

        content_type = ContentType.objects.get_for_model(self)

        if not acting_user:
            raise PermissionDenied(
                "Set permission attempted without providing an acting_user."
            )

        if not self.can_administer(user=acting_user):
            raise PermissionDenied(
                "Acting user does not have administer permissions for this object."
            )

        current_admins = GenericPermission.objects.filter(
            content_type=content_type,
            object_id=self.pk,
            can_administer=True,
        )
        if not can_administer and (
            current_admins.count() == 1
            and (
                (user and user == current_admins[0].user)
                or (team and team == current_admins[0].team)
                or (organization and organization == current_admins[0].organization)
            )
        ):
            raise PermissionDenied(
                "Requested changes would leave no users with administration permissions."
            )

        gp = None
        if user:
            gp, _ = GenericPermission.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=self.pk,
            )
            gp.can_score = can_score or can_write or can_administer
            gp.can_read = can_read or can_write or can_administer
            gp.can_write = can_write or can_administer
            gp.can_administer = can_administer
            gp.save()

        if team:
            gp, _ = GenericPermission.objects.get_or_create(
                team=team,
                content_type=content_type,
                object_id=self.pk,
            )
            gp.can_score = can_score or can_write or can_administer
            gp.can_read = can_read or can_write or can_administer
            gp.can_write = can_write or can_administer
            gp.can_administer = can_administer
            gp.save()

        if organization:
            gp, _ = GenericPermission.objects.get_or_create(
                organization=organization,
                content_type=content_type,
                object_id=self.pk,
            )
            gp.can_score = can_score or can_write or can_administer
            gp.can_read = can_read or can_write or can_administer
            gp.can_write = can_write or can_administer
            gp.can_administer = can_administer
            gp.save()

        # Cache invalidate all users and teams and orgs who have permissions.
        self.clear_permissions_cache()

        return gp

    def clear_permissions_cache(self):
        from organizations.models import GenericPermission

        if hasattr(self, "permissions"):
            del self.permissions

        content_type = ContentType.objects.get_for_model(self)
        class_name = self.__class__.__name__
        types = ["score", "read", "write", "administer"]

        for p in GenericPermission.objects.filter(
            content_type=content_type,
            object_id=self.pk,
        ).all():
            for t in types:
                if p.user:
                    cache.delete(f"permission-pk-{t}-{class_name}-user-{p.user.ox_id}")
                if p.team:
                    cache.delete(f"permission-pk-{t}-{class_name}-team-{p.team.id}")
                if p.organization:
                    cache.delete(
                        f"permission-pk-{t}-{class_name}-organization-{p.organization.id}"
                    )

    def remove_permission(
        self,
        acting_user=None,
        user=None,
        team=None,
        organization=None,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    ):
        from organizations.models import GenericPermission

        content_type = ContentType.objects.get_for_model(self)

        if not acting_user:
            raise PermissionDenied(
                "Set permission attempted without providing an acting_user."
            )

        if not self.can_administer(user=acting_user):
            raise PermissionDenied(
                "Acting user does not have administer permissions for this object."
            )

        current_admins = GenericPermission.objects.filter(
            content_type=content_type,
            object_id=self.pk,
            can_administer=True,
        )
        if not can_administer and (
            current_admins.count() == 1
            and (
                (user and user == current_admins[0].user)
                or (team and team == current_admins[0].team)
                or (organization and organization == current_admins[0].organization)
            )
        ):
            raise PermissionDenied(
                "Requested changes would leave no users with administration permissions."
            )

        if user:
            GenericPermission.objects.filter(
                user=user,
                content_type=content_type,
                object_id=self.pk,
            ).delete()

        if team:
            GenericPermission.objects.filter(
                team=team,
                content_type=content_type,
                object_id=self.pk,
            ).delete()

        if organization:
            GenericPermission.objects.filter(
                organization=organization,
                content_type=content_type,
                object_id=self.pk,
            ).delete()
        if hasattr(self, "permissions"):
            del self.permissions

        return None

    @cached_property
    def permissions(self):
        from organizations.models import GenericPermission

        return {
            "score": {
                "teams": [
                    gp.team
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_score=True,
                    )
                    .exclude(team=None)
                    .distinct("team")
                ],
                "organizations": [
                    gp.organization
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_score=True,
                    )
                    .exclude(organization=None)
                    .distinct("organization")
                ],
                "users": [
                    gp.user
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_score=True,
                    )
                    .exclude(user=None)
                    .distinct("user")
                ],
            },
            "read": {
                "teams": [
                    gp.team
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_read=True,
                    )
                    .exclude(team=None)
                    .distinct("team")
                ],
                "organizations": [
                    gp.organization
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_read=True,
                    )
                    .exclude(organization=None)
                    .distinct("organization")
                ],
                "users": [
                    gp.user
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_read=True,
                    )
                    .exclude(user=None)
                    .distinct("user")
                ],
            },
            "write": {
                "teams": [
                    gp.team
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_write=True,
                    )
                    .exclude(team=None)
                    .distinct("team")
                ],
                "organizations": [
                    gp.organization
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_write=True,
                    )
                    .exclude(organization=None)
                    .distinct("organization")
                ],
                "users": [
                    gp.user
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_write=True,
                    )
                    .exclude(user=None)
                    .distinct("user")
                ],
            },
            "administer": {
                "teams": [
                    gp.team
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_administer=True,
                    )
                    .exclude(team=None)
                    .distinct("team")
                ],
                "organizations": [
                    gp.organization
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_administer=True,
                    )
                    .exclude(organization=None)
                    .distinct("organization")
                ],
                "users": [
                    gp.user
                    for gp in GenericPermission.objects.filter(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        can_administer=True,
                    )
                    .exclude(user=None)
                    .distinct("user")
                ],
            },
        }

    @cached_property
    def organizations(self):
        from organizations.models import GenericPermission

        ct = ContentType.objects.get_for_model(self)
        return [
            gp.organization
            for gp in GenericPermission.objects.filter(
                content_type=ct, object_id=self.id
            ).exclude(organization=None)
        ]

    class Meta:
        abstract = True


class HashidMixin(object):
    ox_id = models.CharField(max_length=254, blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):
        create_ox_id = False
        if not self.ox_id:
            create_ox_id = True
        super(HashidMixin, self).save(*args, **kwargs)

        if create_ox_id:
            self.ox_id = create_unique_ox_id(self.pk, self.__class__, "ox_id")
            self.save()


class HashidModelMixin(models.Model, HashidMixin):
    class Meta:
        abstract = True


class HashidBaseModel(HashidMixin, BaseModel):
    ox_id = models.CharField(max_length=254, blank=True, null=True, db_index=True)

    class Meta:
        abstract = True


class HashidPermissionedModel(HashidMixin, PermissionedModel):
    ox_id = models.CharField(max_length=254, blank=True, null=True, db_index=True)

    class Meta:
        abstract = True


class HasJWTMixin(object):
    oxid = models.CharField(
        blank=True,
        null=True,
        max_length=512,
        unique=True,
        db_index=True,
        editable=False,
    )
    salted_oxid = models.CharField(
        blank=True,
        null=True,
        max_length=512,
        unique=True,
        db_index=True,
        editable=False,
    )
    api_jwt_cached = models.CharField(
        blank=True, null=True, max_length=512, unique=True, editable=False
    )

    def regenerate_api_jwt(self):
        self.api_jwt_cached = jwt.encode(
            {
                "oxid": self.oxid,
                "version": 1,
                "user_type": self.user_type,
            },
            settings.JWT_SECRET,
            algorithm="HS256",
        ).decode()

        return self.api_jwt_cached

    @cached_property
    def api_jwt(self):
        if not self.api_jwt_cached:
            self.api_jwt_cached = self.regenerate_api_jwt()
            self.save()

        return self.api_jwt_cached

    @cached_property
    def events(self):
        from events.models import Event

        return Event.objects.filter(creator=self.oxid)
