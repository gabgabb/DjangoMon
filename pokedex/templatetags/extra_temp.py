from django import template

register = template.Library()


@register.filter
def tabElement(l, i):
    return l[i]

@register.filter
def tabIndex(i):
    return i

@register.filter
def upperCase(s):
    return s.capitalize()
