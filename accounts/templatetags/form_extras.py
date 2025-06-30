from django import template

register = template.Library()

@register.filter
def field_by_name(form, name):
    return form[name]