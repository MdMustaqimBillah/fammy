from django import template

register = template.Library()

@register.filter(name='see_more')
def see_more(value):
    if len(value) > 100:
        result = []
        result = value[0:100]
    else:
        result = value
    return result



@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='index')
def index(list):
    return list[0]
