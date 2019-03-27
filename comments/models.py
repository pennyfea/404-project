from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

# Create your models here.


class CommentManager(models.Manager):
    def all(self):
        query_set = super(CommentManager, self).filter(parent=None)
        return query_set

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        query_set = super(CommentManager, self).filter(
            content_type=content_type, object_id=obj_id).filter(parent=None)
        return query_set


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=36)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['published']

    # replies
    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
