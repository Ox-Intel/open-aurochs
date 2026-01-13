from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from organizations.models import User
from history.models import ObjectHistoryChange
from utils.helpers import rel
from utils.encryption import create_unique_ox_id
from utils.models import BaseModel, SubscribableMixin, HashidModelMixin, HashidBaseModel


class ObjectSubscription(BaseModel):
    user_specific_caching = True
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(SubscribableMixin, HashidBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    body = models.TextField(blank=True, null=True)
    edited = models.BooleanField(default=False)

    def to_data(self, requesting_user):
        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "user": rel(self, "user"),
            "body": self.body,
            "edited": self.edited,
            "react_url": self.react_url,
            "vue_url": self.vue_url,
            "created_by": rel(self, "created_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = [
            self.user,
        ]
        objs.append(self.created_by)
        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []
        for ii in InboxItem.objects.filter(comment=self).all():
            objs.append(ii.user)

        return objs

    @property
    def react_url(self):
        return f"/{self.content_type.name}/{self.object_id}"

    @property
    def vue_url(self):
        return f"/{self.content_type.name}/{self.object_id}"


class InboxItem(BaseModel):
    user_specific_caching = True
    # user = whose inbox this is.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change = models.ForeignKey(
        ObjectHistoryChange, blank=True, null=True, on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment, blank=True, null=True, on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    read = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    ox_id = models.CharField(max_length=254, blank=True, null=True, db_index=True)

    def to_data(self, requesting_user):
        return {
            "id": self.ox_id,
            "ox_id": self.ox_id,
            "initiator": rel(self, "initiator"),
            "type": self.content_type.model.lower(),
            "target": rel(self, "content_object"),
            "comment": rel(self, "comment"),
            "user": rel(self, "user"),
            "body": self.body,
            "read": self.read,
            "done": self.done,
            "change_type": self.change_type,
            "created_by": rel(self, "created_by"),
            "created_at_ms": self.created_at_ms,
            "modified_at_ms": self.modified_at_ms,
        }

    def child_objects(self, requesting_user):
        # Objects that we want to include in the data dump so that the to_data reference is filled out.
        objs = [
            self.user,
        ]
        if self.initiator:
            objs.append(self.initiator)
        if self.content_object and self.content_object.can_know_exists(
            user=requesting_user
        ):
            objs.append(self.content_object)
            if self.content_object and hasattr(self.content_object, "child_objects"):
                objs.extend(self.content_object.child_objects(requesting_user))
        if self.comment:
            objs.append(self.comment)
        if self.created_by:
            objs.append(self.created_by)

        return objs

    def parent_objects(self, requesting_user=None):
        # Objects that we want to cache invalidate if this object changes.
        # !! Because they have indirect/calculated properties, not simply because they foreign key to it.

        objs = []

        return objs

    def save(self, *args, **kwargs):
        create_ox_id = False
        if not self.ox_id:
            create_ox_id = True
        super(InboxItem, self).save(*args, **kwargs)

        if create_ox_id:
            self.ox_id = create_unique_ox_id(self.pk, self.__class__, "ox_id")
            self.save()

    @property
    def target(self):
        return self.content_object

    @property
    def change_type(self):
        if self.change:
            return self.change.change_type
        return ""

    @property
    def body(self):
        if self.comment:
            return self.comment.body

        if self.change:
            return self.change.description
        return ""

    @property
    def initiator(self):
        if self.comment:
            return self.comment.user

        if self.change:
            return self.change.changed_by
        return ""


@receiver(post_save, sender=Comment)
def comment_saved(sender, instance, created, **kwargs):
    from collaboration.models import InboxItem, ObjectSubscription

    if created:
        for os in (
            ObjectSubscription.objects.filter(
                object_id=instance.object_id, content_type=instance.content_type
            )
            .exclude(deleted=True)
            .distinct()
        ):
            if instance.user != os.user:
                ii, _ = InboxItem.objects.get_or_create(
                    user=os.user,
                    object_id=os.object_id,
                    content_type=os.content_type,
                )
                ii.comment = instance
                ii.read = False
                ii.done = False
                ii.save()

        try:
            ii = InboxItem.objects.get(
                user=instance.user,
                object_id=instance.object_id,
                content_type=instance.content_type,
            )
            ii.comment = instance
            ii.save()
        except InboxItem.DoesNotExist:
            pass
