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


register.filter('text', text)
register.filter('user_id', user_id)
