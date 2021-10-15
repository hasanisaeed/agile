from django import template

register = template.Library()


def text(v):
    import ast
    v = ast.literal_eval(v.message)
    return v['text']


register.filter('text', text)
