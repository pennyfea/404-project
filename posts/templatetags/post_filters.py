from django import template
from users.models import User
import re

register = template.Library()


@register.filter(name='get_author_name')
def get_author_name(value1):
    if (isinstance(value1, dict)):
        return (value1['author']['displayName'])
    else:
        return value1.user


@register.filter(name='get_author_id')
def get_author_id(value1):
    if (isinstance(value1, dict)):
        host = re.sub('^https?:\/\/', '', value1['author']['id'])
        host = re.sub('\/', '', host)
        return (host)
    else:
        id = User.objects.filter(username=value1.user)[0].id
        return id


@register.filter(name='get_privacy')
def get_privacy(value1):
    if (isinstance(value1, dict)):
        return (value1['visibility'])
    else:
        return value1.get_privacy_display()


@register.filter(name='get_comment_author')
def get_comment_author(value1):
    # print(value1)
    if (isinstance(value1, dict)):
        return (value1['author']['displayName'])
    else:
        return value1.user


@register.filter(name='get_comment_content')
def get_comment_content(value1):
    # print(value1)
    if (isinstance(value1, dict)):
        return (value1['comment'])
    else:
        return value1.content
