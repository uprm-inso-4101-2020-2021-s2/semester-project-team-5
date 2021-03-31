from django import template

from cart.models import cart_item

register = template.Library()

@register.simple_tag
def quantity(cart, item):
    return cart_item.objects.get(cart_id=cart.pk, item_id=item.pk).quantity