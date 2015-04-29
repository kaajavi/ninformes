from django import template

register = template.Library()

@register.simple_tag
def increment_counter(outer, inner, outer_loop_length):
    num = (outer + inner * outer_loop_length + inner * (outer_loop_length - 1))
    num = num +1
    ret = str(num).rjust(3).replace(' ','0')
    return ret


