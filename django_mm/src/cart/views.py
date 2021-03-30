from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from items.models import Item
from .models import Cart, Order
from users.forms import LoginForm


def get_or_update_cart(request, user):
    cart_obj = None
    qs = Cart.objects.filter(user_id=user.pk, checkout=False)
    if qs.exists():
        cart_obj = qs.last()
        if request.session.get('cart_id', None) is not None:
            session_cart = Cart.objects.get(pk=request.session['cart_id'])
            for item in session_cart.items.all():
                cart_obj.items.add(item)
            session_cart.delete()
    elif request.session.get('cart_id', None) is not None:
       cart_obj = Cart.objects.get(pk=request.session['cart_id'])
       if cart_obj.user is None:
            cart_obj.user_id = user.pk
            cart_obj.save()

    if cart_obj is None:
        cart_obj = Cart.objects.new(user)

    return cart_obj


# @login_required(login_url='/users/login/')
def cart_home(request):
    cart_obj = Cart.objects.get(pk=request.session['cart_id'])
    request.session['cart_total'] = cart_obj.items.count()
    return render(request, "cart/main.html", {"cart": cart_obj})


def cart_update(request):
    item_id = request.POST.get('item')
    if item_id is not None:
        try:
            item_obj = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            print("Show message to user, item is gone")
            return redirect('cart:cart_home')

        if not request.user.is_authenticated and request.session.get("cart_id", None) is None:
            cart_obj = Cart.objects.new()
            request.session['cart_id'] = cart_obj.id
        else:
            cart_obj = Cart.objects.get(pk=request.session['cart_id'])

        if item_obj in cart_obj.items.all():
            cart_obj.items.remove(item_obj)
        else:
            cart_obj.items.add(item_obj)
        request.session['cart_total'] = cart_obj.items.count()
    return redirect('cart:cart_home')


def checkout_home(request):

    cart_id = request.session.get("cart_id", None)
    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        cart_created = False
        cart_obj = qs.first()
        if request.user.is_authenticated and cart_obj.user is None:  # once it gets authenticated it changes to that user
            cart_obj.user = request.user
            cart_obj.save()
    else:
        cart_obj = Cart.objects.new(user=request.user)
        cart_created = True
        request.session['cart_id'] = cart_obj.id
    order_obj = None
    if cart_created or cart_obj.items.count() == 0:
        return redirect('cart:cart_home')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
        user = request.user
        # billing_profile =
        # login_form = LoginForm()
        # if user.is_authenticated:
        #     billing_profile = None

        context = {
            "object": order_obj,
            "billing": billing_profile,
            "loginform": login_form
        }

    return render(request, "cart/checkout.html", context)
