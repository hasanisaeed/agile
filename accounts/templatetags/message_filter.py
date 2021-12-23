import json

from django import template

register = template.Library()


def text(v):
    import ast
    v = ast.literal_eval(v.message)
    return v['text']


def user_id(v):
    import ast
    v = ast.literal_eval(v.message)
    return v['user']


def to_json(v):
    return v


register.filter('text', text)
register.filter('user_id', user_id)
register.filter('to_json', to_json)
