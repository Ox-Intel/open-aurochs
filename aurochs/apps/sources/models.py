from django.db import models
from django.utils.functional import cached_property
from django.utils import timezone

from organizations.models import Organization
from utils.helpers import rel
from utils.models import PermissionedModel, HashidPermissionedModel, BaseModel


class Source(HashidPermissionedModel):
    user_specific_caching = True
    name = models.TextField(null=True)
    subtitle = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    @classmethod
    def values_dict_to_data(self, requesting_user, all_user_data):
        from reports.models import Report

        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "notes": self.notes,
            "created_by": rel(self, "created_by"),
            "modified_by": rel(self, "modified_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            "permissions": self.permissions_dict,
            "report_id_list": [
                r.id
                for r in self.all_of_type_in_user_objects(
                    "reports", "sources", all_user_data
                )
            ],
            "subscribed": self.subscribed(requesting_user),
            "tags": [rel(t) for t in self.tags(requesting_user)],
            "comments": [rel(c) for c in self.comments],
            "subscribers": [rel(u) for u in self.subscribers],
            "search_text": self.search_text(requesting_user),
        }

    def to_data(self, requesting_user):
        from reports.models import Report

        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "name": self.name,
            "subtitle": self.subtitle,
            "notes": self.notes,
            "created_by": rel(self, "created_by"),
            "modified_by": rel(self, "modified_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
            "permissions": self.permissions_dict,
            "report_id_list": [
                r
                for r in Report.authorized_objects.authorize(user=requesting_user)
                .findable.filter(sources=self)
                .values_list("id", flat=True)
            ],
            "subscribed": self.subscribed(requesting_user),
            "tags": [rel(t) for t in self.tags(requesting_user)],
            "comments": [rel(c) for c in self.comments],
            "subscribers": [rel(u) for u in self.subscribers],
            "search_text": self.search_text(requesting_user),
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = []
        objs.append(self.created_by)
        objs.extend([o for o in self.comments])
        objs.extend([c.user for c in self.comments])
        objs.extend([s for s in self.subscribers])
        objs.extend([t for t in self.tags(requesting_user)])
        objs.extend([c.created_by for c in self.comments])
        # objs = [sf for sf in self.source_feedback_set.all()]

        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.
        from reports.models import Report

        objs = []
        if requesting_user:
            objs.append(requesting_user)
            objs.extend(
                [
                    r
                    for r in Report.authorized_objects.authorize(user=requesting_user)
                    .findable.filter(sources=self)
                    .all()
                ]
            )
        else:
            objs.extend([r for r in Report.objects.filter(sources=self).all()])
        return objs

    api_writable_fields = [
        "name",
        "subtitle",
        "notes",
    ]

    def __str__(self):
        return self.name or ""

    @cached_property
    def report_id_list(self):
        return [
            i
            for i in self.report_set.exclude(deleted=True).values_list("pk", flat=True)
        ]


class SourceFeedback(BaseModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    score = models.IntegerField(blank=True, null=True)

    def to_data(self, requesting_user):
        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "score": self.score,
            "source": rel(self, "source"),
            "created_by": rel(self, "created_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = [
            self.source,
        ]
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        if requesting_user:
            objs.append(requesting_user)
            objs.extend(
                [
                    r
                    for r in Source.authorized_objects.authorize(user=requesting_user)
                    .findable.filter(source=self.source)
                    .all()
                ]
            )
        else:
            objs.extend([r for r in Source.objects.filter(source=self.source).all()])

        return objs

    api_writable_fields = [
        "source",
        "score",
    ]

    def __str__(self):
        return self.source or ""
