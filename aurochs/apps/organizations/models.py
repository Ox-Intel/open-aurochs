from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.db.models import Q
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from utils.encryption import create_unique_ox_id
from utils.helpers import reverse, rel
from utils.models import (
    BaseModel,
    HashidPermissionedModel,
    HasJWTMixin,
    BaseManager,
    PermissionedModel,
    HashidMixin,
    HashidBaseModel,
    DataDictMixin,
)


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, password=None):
        u = self.create(username=username)
        u.set_password(password)
        u.save()
        return u

    def create_superuser(self, username, password):
        u = self.create_user(username, password)
        u.is_superuser = True
        u.is_active = True
        u.is_ox_staff = True
        u.save()
        return u


class User(AbstractBaseUser, PermissionsMixin, DataDictMixin, HasJWTMixin, HashidMixin):
    user_specific_caching = True
    USERNAME_FIELD = "username"

    username = models.CharField(
        unique=True,
        max_length=4096,
        blank=True,
        null=True,
    )
    password = models.CharField(max_length=255)
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    ox_id = models.CharField(max_length=254, blank=True, null=True, db_index=True)
    # TODO: Not unique=True?  Legacy data has collisions.
    email = models.CharField(
        max_length=4096,
        blank=True,
        null=True,
    )
    email_verified = models.BooleanField(default=False)
    time_zone = models.CharField(max_length=254, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    modified_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    is_ox_staff = models.BooleanField(default=False)
    public_signup = models.BooleanField(default=False)

    pinned_stack = models.ForeignKey(
        "stacks.Stack", null=True, blank=True, on_delete=models.SET_NULL
    )
    pinned_framework = models.ForeignKey(
        "frameworks.Framework", null=True, blank=True, on_delete=models.SET_NULL
    )
    pinned_report = models.ForeignKey(
        "reports.Report", null=True, blank=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        create_ox_id = False
        if not self.ox_id:
            create_ox_id = True
        super(User, self).save(*args, **kwargs)

        if create_ox_id:
            self.ox_id = create_unique_ox_id(self.pk, self.__class__, "ox_id")
            self.save()

    objects = UserManager()

    @cached_property
    def lines_cache_key(self):
        return f"{self.ox_id}-lines-cache"

    @cached_property
    def color_index(self):
        return self.id % 21

    def cached_data_lines(self):
        return cache.get(self.lines_cache_key, "")

    def save_data_lines_to_cache(self, data_lines):
        return cache.set(self.lines_cache_key, data_lines)

    def to_data(self, requesting_user):
        self.teams_requester_can_see(requesting_user)
        self.orgs_requester_can_see(requesting_user)

        d = {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "initials": self.initials,
            "time_zone": self.time_zone,
            "teams": [rel(t) for t in self.teams_requester_can_see(requesting_user)],
            "organizations": [
                rel(o) for o in self.orgs_requester_can_see(requesting_user)
            ],
        }
        if requesting_user == self:
            d["pinned_report_pk"] = self.pinned_report_pk
            d["pinned_stack_pk"] = self.pinned_stack_pk
            d["pinned_framework_pk"] = self.pinned_framework_pk
            d["averages"] = self.averages
            d["inbox"] = self.inbox
            d["email"] = self.email
        return d

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = []
        objs.extend([o for o in self.teams_requester_can_see(requesting_user)])
        objs.extend([o for o in self.orgs_requester_can_see(requesting_user)])
        if requesting_user == self:
            objs.append(self.pinned_framework)
            objs.append(self.pinned_report)
            objs.append(self.pinned_stack)
            for ii in self.inbox_items:
                objs.append(ii)
                objs.extend(ii.child_objects(requesting_user))

        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        if requesting_user:
            objs.append(requesting_user)

        return objs

    def __str__(self):
        return self.username

    def teams_requester_can_see(self, requesting_user):
        visible_teams = []
        for t in self.teams:
            if t in requesting_user.teams:
                visible_teams.append(t)
        return visible_teams

    def orgs_requester_can_see(self, requesting_user):
        if self == requesting_user:
            return self.organizations

        visible_orgs = []
        for o in self.organizations:
            if o in requesting_user.organizations:
                visible_orgs.append(o)
        return visible_orgs

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def pinned_framework_pk(self):
        if self.pinned_framework:
            return self.pinned_framework.pk
        return None

    @property
    def pinned_report_pk(self):
        if self.pinned_report:
            return self.pinned_report.pk
        return None

    @property
    def pinned_stack_pk(self):
        if self.pinned_stack:
            return self.pinned_stack.pk
        return None

    @property
    def initials(self):
        initials_str = ""
        if self.first_name:
            initials_str = self.first_name[0]
        if self.last_name:
            initials_str += self.last_name[0]

        return initials_str

    @cached_property
    def teams(self):
        return [
            tm.team
            for tm in self.teammember_set.prefetch_related("team")
            .exclude(team__deleted=True)
            .distinct()
            .order_by("-created_at")
            .all()
        ]

    @cached_property
    def organizations(self):
        return [
            orgrole.organization
            for orgrole in self.organizationrole_set.prefetch_related("organization")
            .exclude(organization__deleted=True)
            .order_by("-created_at")
            .distinct()
            .all()
        ]

    @property
    def is_staff(self):
        return self.is_ox_staff

    @property
    def averages(self):
        from reports.models import ScorecardScore

        d = {"criteria": {}}
        avgs = {"criteria": {}}
        for scs in ScorecardScore.objects.filter(
            scorecard__scorer=self, deleted=False, scorecard__deleted=False
        ).all():
            if scs.score is not None:
                if f"criteria__{scs.criteria.pk}" not in avgs["criteria"]:
                    avgs["criteria"][f"criteria__{scs.criteria.pk}"] = {}
                    avgs["criteria"][f"criteria__{scs.criteria.pk}"]["num"] = 0
                    avgs["criteria"][f"criteria__{scs.criteria.pk}"]["total"] = 0

                avgs["criteria"][f"criteria__{scs.criteria.pk}"]["total"] += scs.score
                avgs["criteria"][f"criteria__{scs.criteria.pk}"]["num"] += 1

        for k, c in avgs["criteria"].items():
            d["criteria"][k] = c["total"] / c["num"]
        return d

    @property
    def inbox(self):
        inbox = {
            "active": [],
            "done": [],
            "unread_count": self.inbox_items.filter(read=False, done=False).count(),
        }
        for ii in self.inbox_items:
            if ii.done:
                inbox["done"].append(f"{ii.ox_id}")
            else:
                inbox["active"].append(f"{ii.ox_id}")
        return inbox

    @cached_property
    def inbox_items(self):
        from collaboration.models import InboxItem

        return InboxItem.objects.filter(user=self, deleted=False).all().distinct()


class Organization(HashidBaseModel):
    user_specific_caching = True
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    api_writable_fields = [
        "name",
        "description",
    ]
    excluded_fields = [
        "created_by",
        "modified_by",
    ]

    def to_data(self, requesting_user):
        members = []
        if self.is_member(requesting_user):
            members = [
                {
                    "id": org_role.user.ox_id,
                    "can_view": org_role.can_view,
                    "can_manage": org_role.can_manage,
                }
                for org_role in self.organizationrole_set.exclude(deleted=True)
                .all()
                .order_by(
                    "-can_manage", "-can_view", "user__first_name", "user__last_name"
                )
            ]

        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "name": self.name,
            "description": self.description,
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            "members": members,
            "num_reports": self.num_reports,
            "num_frameworks": self.num_frameworks,
            "num_sources": self.num_sources,
            "last_admin_for": [rel(o) for o in self.last_admin_for(requesting_user)],
            "can_be_deleted": self.can_be_deleted,
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = []
        if self.is_member(requesting_user):
            objs.extend(self.members)
        objs.extend(self.last_admin_for(requesting_user))
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        if requesting_user:
            objs.append(requesting_user)

    def __str__(self):
        return self.name or ""

    def add_user(self, user, can_view=True, can_manage=False):
        org_role, _ = OrganizationRole.objects.get_or_create(
            user=user, organization=self
        )
        org_role.can_view = can_view
        org_role.can_manage = can_manage
        org_role.save()

        self.clear_permissions_cache(user_changed=user)
        return org_role

    def remove_user(self, user):
        OrganizationRole.objects.filter(user=user, organization=self).delete()
        self.clear_permissions_cache(user_changed=user)

    def clear_permissions_cache(self, user_changed=None):
        permissioned_models = ["Report", "Framework", "Source"]
        types = ["score", "read", "write", "administer"]
        for t in types:
            for p in permissioned_models:
                if user_changed:
                    cache.delete(f"permission-pk-{t}-{p}-user-{user_changed.ox_id}")
                cache.delete(f"permission-pk-{t}-{p}-organization-{self.id}")

    def is_member(self, requesting_user):
        return (
            self.organizationrole_set.exclude(deleted=True)
            .filter(user=requesting_user)
            .filter(Q(can_manage=True) | Q(can_view=True))
            .count()
            > 0
        )

    @property
    def members(self):
        return [
            org_role.user
            for org_role in self.organizationrole_set.exclude(deleted=True).all()
        ]

    def last_admin_for(self, requesting_user):
        objs = []
        for gp in GenericPermission.objects.filter(
            organization=self, can_administer=True
        ):
            if (
                GenericPermission.objects.filter(
                    can_administer=True,
                    content_type=gp.content_type,
                    object_id=gp.object_id,
                )
                .exclude(organization=self)
                .count()
                == 0
            ):
                if gp.content_object and gp.content_object.can_know_exists(
                    user=requesting_user
                ):
                    objs.append(gp.content_object)
        return objs

    @property
    def can_be_deleted(self):
        for gp in GenericPermission.objects.filter(
            organization=self, can_administer=True
        ):
            if (
                GenericPermission.objects.filter(
                    can_administer=True,
                    content_type=gp.content_type,
                    object_id=gp.object_id,
                )
                .exclude(organization=self)
                .count()
                == 0
            ):
                return False
        return True

    @property
    def num_reports(self):
        return GenericPermission.objects.filter(
            Q(can_administer=True)
            | Q(can_read=True)
            | Q(can_write=True)
            | Q(can_score=True),
            content_type__app_label="reports",
            content_type__model="report",
            organization=self,
        ).count()

    @property
    def num_frameworks(self):
        return GenericPermission.objects.filter(
            Q(can_administer=True)
            | Q(can_read=True)
            | Q(can_write=True)
            | Q(can_score=True),
            content_type__app_label="frameworks",
            content_type__model="framework",
            organization=self,
        ).count()

    @property
    def num_sources(self):
        return GenericPermission.objects.filter(
            Q(can_administer=True)
            | Q(can_read=True)
            | Q(can_write=True)
            | Q(can_score=True),
            content_type__app_label="sources",
            content_type__model="source",
            organization=self,
        ).count()

    def can_manage(self, requesting_user):
        return (
            self.organizationrole_set.exclude(deleted=True)
            .filter(user=requesting_user, can_manage=True)
            .count()
            > 0
        )

    def can_view(self, requesting_user):
        return (
            self.organizationrole_set.exclude(deleted=True)
            .filter(user=requesting_user, can_view=True)
            .count()
            > 0
        )


class OrganizationRole(BaseModel):
    # role = models.CharField(max_length=20, null=True, choices=ORGANIZATION_ROLES)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_manage = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.organization}"


class Team(HashidBaseModel):
    user_specific_caching = True
    """
    Teams are just groupings of people within an organization.
    There also exist all-organization "teams" and personal "teams".
    """

    name = models.CharField(max_length=1000, null=True)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    api_writable_fields = [
        "name",
        "description",
    ]

    def to_data(self, requesting_user):
        members = []
        if self.is_member(requesting_user) or self.organization.can_manage(
            requesting_user
        ):
            members = [
                {
                    "id": team_member.user.ox_id,
                    "can_view": team_member.can_view,
                    "can_manage": team_member.can_manage,
                }
                for team_member in self.teammember_set.exclude(deleted=True)
                .all()
                .order_by(
                    "-can_manage", "-can_view", "user__first_name", "user__last_name"
                )
            ]

        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "name": self.name,
            "description": self.description,
            "organization": rel(self, "organization"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            "members": members,
            "num_reports": self.num_reports,
            "num_frameworks": self.num_frameworks,
            "num_sources": self.num_sources,
            "last_admin_for": [rel(o) for o in self.last_admin_for(requesting_user)],
            "can_be_deleted": self.can_be_deleted,
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = [self.organization]
        if self.is_member(requesting_user):
            objs.extend(self.members)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        if requesting_user:
            objs.append(requesting_user)

    excluded_fields = [
        "created_by",
        "modified_by",
    ]

    def __str__(self):
        return f"{self.name} - {self.organization}"

    def add_user(self, user, can_view=True, can_manage=False):
        tm, _ = TeamMember.objects.get_or_create(user=user, team=self)
        tm.can_view = can_view
        tm.can_manage = can_manage
        tm.save()

        # Need to clear the permissions cache for the team and this user.
        self.clear_permissions_cache(user_changed=user)

        return tm

    def remove_user(self, user):
        TeamMember.objects.filter(user=user, team=self).delete()
        self.clear_permissions_cache(user_changed=user)

    def clear_permissions_cache(self, user_changed=None):
        permissioned_models = ["Report", "Framework", "Source"]
        types = ["score", "read", "write", "administer"]
        for t in types:
            for p in permissioned_models:
                if user_changed:
                    cache.delete(f"permission-pk-{t}-{p}-user-{user_changed.ox_id}")
                cache.delete(f"permission-pk-{t}-{p}-team-{self.id}")

    def is_member(self, requesting_user):
        return (
            self.teammember_set.exclude(deleted=True)
            .filter(user=requesting_user)
            .filter(Q(can_manage=True) | Q(can_view=True))
            .count()
            > 0
        )

    @property
    def members(self):
        return [tm.user for tm in self.teammember_set.exclude(deleted=True).all()]

    def last_admin_for(self, requesting_user):
        objs = []
        for gp in GenericPermission.objects.filter(team=self, can_administer=True):
            if (
                GenericPermission.objects.filter(
                    can_administer=True,
                    content_type=gp.content_type,
                    object_id=gp.object_id,
                )
                .exclude(team=self)
                .count()
                == 0
            ):
                if gp.content_object.can_know_exists(user=requesting_user):
                    objs.append(gp.content_object)
        return objs

    @property
    def can_be_deleted(self):
        for gp in GenericPermission.objects.filter(team=self, can_administer=True):
            if (
                GenericPermission.objects.filter(
                    can_administer=True,
                    content_type=gp.content_type,
                    object_id=gp.object_id,
                )
                .exclude(team=self)
                .count()
                == 0
            ):
                return False
        return True

    @property
    def num_reports(self):
        return GenericPermission.objects.filter(
            Q(can_administer=True)
            | Q(can_read=True)
            | Q(can_write=True)
            | Q(can_score=True),
            content_type__app_label="reports",
            content_type__model="report",
            team=self,
        ).count()

    @property
    def num_frameworks(self):
        return GenericPermission.objects.filter(
            Q(can_administer=True)
            | Q(can_read=True)
            | Q(can_write=True)
            | Q(can_score=True),
            content_type__app_label="frameworks",
            content_type__model="framework",
            team=self,
        ).count()

    @property
    def num_sources(self):
        return GenericPermission.objects.filter(
            Q(can_administer=True)
            | Q(can_read=True)
            | Q(can_write=True)
            | Q(can_score=True),
            content_type__app_label="sources",
            content_type__model="source",
            team=self,
        ).count()

    def can_manage(self, requesting_user):
        return (
            self.teammember_set.exclude(deleted=True)
            .filter(user=requesting_user, can_manage=True)
            .count()
            > 0
        )

    def can_view(self, requesting_user):
        return (
            self.teammember_set.exclude(deleted=True)
            .filter(user=requesting_user, can_view=True)
            .count()
            > 0
        )


class TeamMember(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_manage = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team} - {self.user}"


class GenericPermission(DataDictMixin, models.Model):
    """
    TODO: This will become a permissions UI like:
            View     Edit    Manage
    Org A     X                X
    Team A    X       X        X
    Team B                     X
    User C    X       X
    Me        X       X        X
    [+ Add]
    UI does not allow all owners to be unchecked.
    """

    created_at = models.DateTimeField(
        db_index=True, blank=True, null=True, default=timezone.now
    )
    modified_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    deleted = models.BooleanField(null=True, default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords(inherit=True)

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        Organization, blank=True, null=True, on_delete=models.CASCADE
    )
    can_score = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_administer = models.BooleanField(default=False)


class Tag(HashidBaseModel):
    name = models.CharField(blank=False, null=False, max_length=512)
    slug = models.CharField(blank=True, null=False, max_length=512)
    organization = models.ForeignKey(
        Organization, blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def to_data(self, requesting_user):
        return {
            "id": self.ox_id,
            "name": self.name,
            "user": rel(self, "user"),
            "organization": rel(self, "organization"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = [
            self.user,
            self.organization,
        ]
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        for tt in TaggedObject.objects.filter(tag=self).all():
            objs.append(tt.content_object)

        return objs


class TaggedObject(BaseModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")
