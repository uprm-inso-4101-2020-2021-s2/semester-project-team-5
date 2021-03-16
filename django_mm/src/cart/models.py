from decimal import *
from django.db import models
from django.conf import settings
from items.models import Item
from django.db.models.signals import pre_save, post_save, m2m_changed

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user       = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    items       = models.ManyToManyField(Item, blank=True)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)  # when the cart was created

    objects = CartManager()

    def __str__(self):
        return str(self.id)


# method to recalculate price after removing or adding items
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        items = instance.items.all()
        total = 0
        for eachitem in items:
            total += eachitem.price
        instance.subtotal = total
        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.items.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    # Puerto Rico tax is 10.5%
    if instance.subtotal > 0:
        instance.total = instance.subtotal + Decimal((instance.subtotal * Decimal(0.105)))
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)

