# coding=utf8
from django import template

register = template.Library()

#
# @stringfilter
# def truncatehanzi(value, arg):
#     """
#     Truncates a string after a certain number of words including
#     alphanumeric and CJK characters.
#     Argument: Number of words to truncate after.
#     """
#     try:
#         bits = []
#         for x in arg.split(u':'):
#             if len(x) == 0:
#                 bits.append(None)
#             else:
#                 bits.append(int(x))
#         if int(x) < len(value):
#             return value[slice(*bits)] + '...'
#         return value[slice(*bits)]
#
#     except (ValueError, TypeError):
#         return value  # Fail silently.
#
#
# register.filter('truncatehanzi', truncatehanzi)


@register.filter(name="is_none_or_blank")
def is_none_or_blank(value):
    if isinstance(value, str):
        if value is None or len(value.strip()) == 0:
            return True
    return False


@register.filter(name="change_line_break_to_br")
def change_line_break_to_br(value):
    if isinstance(value, str):
        value = value.replace('\n', '<br>')
    return value


@register.filter(name="my_slice")
def change_line_break_to_br(value, length):
    """切分, 从第一个开始, 给定长度"""
    if isinstance(length, int) and length > 0:
        return value[:length]
    else:
        return value
