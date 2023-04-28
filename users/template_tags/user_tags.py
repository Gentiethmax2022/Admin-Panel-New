from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag
def get_current_user_groups(user):
    return [g.name for g in user.groups.all()]


