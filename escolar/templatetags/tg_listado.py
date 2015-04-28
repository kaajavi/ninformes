from django import template

register = template.Library()

@register.simple_tag
def increment_counter(outer, inner, outer_loop_length):
    return (outer + inner * outer_loop_length + inner * (outer_loop_length - 1)) + 1


