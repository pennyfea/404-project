from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser


# TODO: Will need to add UUIDs at some point.
# TODO: When using UUIDs the username column will need to be UNIQUE
class User(AbstractUser):

    host = models.TextField(max_length=500, blank=False) # Their host
    url = models.TextField(max_length=500, blank=False) # Url to their profile page
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    bio = models.TextField(max_length=500, blank=True)
    github = models.TextField(max_length=500, blank=True) # TODO: Find reasonable length
    is_active = models.BooleanField(('active'), default=False)
    is_admin = models.BooleanField(('admin'), default=False)

    def __str__(self):
        return self.username
        

class Node(models.Model):

    host = models.CharField(max_length = 500) # TODO: Find reasonable length
    sharing = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class NodeSetting(models.Model):

    id = models.IntegerField(default=1, primary_key=True)
    #node_limit = models.IntegerField(default=10,  help_text='The maximum number of servers that should be connected at one time.')
    require_auth = models.BooleanField(default=True, help_text='Specify if incoming server connections require authentication.')
    share_posts = models.BooleanField(default=True, help_text='Specify if posts should be shared with other servers.')
    share_imgs = models.BooleanField(default=True, help_text='Specify if images should be shared with other servers.')

    # Override database save method to force a max of one entry in the table
    def save(self, *args, **kwargs):
        if NodeSetting.objects.count() == 1:
            NodeSetting.objects.all()[0].delete()
        super(NodeSetting, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
