from django import template

register = template.Library()

@register.filter
def replace_slash(value):
    return value.replace('\\', '/')
