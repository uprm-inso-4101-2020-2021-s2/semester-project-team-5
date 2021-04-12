from django import template

from cart.models import CartItem

register = template.Library()

@register.simple_tag
def quantity(cart, item):
    return CartItem.objects.get(cart_id=cart.pk, item_id=item.pk).quantity