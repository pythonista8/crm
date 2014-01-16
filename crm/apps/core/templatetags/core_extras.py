from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='attributes')
def attrs(value, arg):
    """Set attributes of an HTML element.

    Syntax:
        {{ element|attributes:"class: sample_class, id: sample_id" }}
    """
    attrs = value.field.widget.attrs
    for string in arg.split(','):
        if ':' in string:
            kv = string.split(':')
            attrs[kv[0]] = mark_safe(kv[1].strip())
        else:
            kv = string.strip()
            attrs[kv] = mark_safe(kv)
    return str(value)


@register.filter(name='modelname')
def modelname(value):
    name = value._meta.verbose_name.title()
    if not name:
        name = value.__class__.__name__
    return name


@register.filter(name='times')
def times(num):
    """Make list from a given number.

    Syntax:
        {{ 15|times }}
    """
    return range(num)
