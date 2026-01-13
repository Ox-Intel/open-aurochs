from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from organizations.models import User
from utils.models import BaseModel


class DeletedUser:
    pass


class ObjectHistoryChange(BaseModel):
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    change_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    changed_by_id = models.PositiveIntegerField()
    changed_by_name = models.CharField(max_length=512)

    def changed_by(self):
        try:
            return User.objects.get(pk=self.changed_by_id)
        except User.DoesNotExist:
            obj = DeletedUser()
            obj.name = self.changed_by_name
            obj.id = self.changed_by_id
            return obj


@receiver(post_save, sender=ObjectHistoryChange)
def object_history_saved(sender, instance, created, **kwargs):
    from collaboration.models import InboxItem, ObjectSubscription

    if created:
        for os in ObjectSubscription.objects.filter(
            object_id=instance.object_id, content_type=instance.content_type
        ):
            ii, _ = InboxItem.objects.get_or_create(
                user=os.user,
                change=instance,
                object_id=instance.object_id,
                content_type=instance.content_type,
            )
            ii.change = instance
            ii.read = False
            ii.done = False
            ii.save()
