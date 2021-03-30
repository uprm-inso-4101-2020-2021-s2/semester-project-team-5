from decimal import *
import math
import random
import string
from django.db import models
from django.conf import settings
from items.models import Item
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

ORDER_STATUS_CHOICES  = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),

)


class CartManager(models.Manager):

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user            = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    items           = models.ManyToManyField(Item, blank=True)
    total           = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal        = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)  # when the cart was created+
    checkout = models.BooleanField(default=False)

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


class Order(models.Model):
    order_id        = models.CharField(max_length=120, blank=True)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=120, default="created", choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    order_total     = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        total = math.fsum([cart_total, shipping_total]).__format__('.2f')
        print(total)
        self.order_total = total
        self.save()
        return total
    

# signals to handle a unique order id
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def unique_order_id_generator(instance):
    order_id = random_string_generator()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


# each time cart changes
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


# new order (it was just created)
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
