from django.shortcuts import render, redirect
from items.models import Item
from .models import Cart, Order
from users.forms import LoginForm


def cart_home(request):

    # check if a cart is created, in order to not create a new one
    cart_id = request.session.get("cart_id", None)
    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        print("Cart ID exists")
        cart_obj = qs.first()
        if request.user.is_authenticated and cart_obj.user is None:  # once it gets authenticated it changes to that user
            cart_obj.user = request.user
            cart_obj.save()
    else:
        cart_obj = Cart.objects.new(user=request.user)
        request.session['cart_id'] = cart_obj.id

    return render(request, "cart/main.html", {"cart": cart_obj})


def cart_update(request):
    item_id = request.POST.get('item')
    if item_id is not None:

        try:
            item_obj = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            print("Show message to user, item is gone")
            return redirect('cart:cart_home')

        cart_id = request.session.get("cart_id", None)
        qs = Cart.objects.filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:  # once it gets authenticated it changes to that user
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id

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
        billing_profile = None
        login_form = LoginForm()
        if user.is_authenticated:
            billing_profile = None

        context = {
            "object": order_obj,
            "billing": billing_profile,
            "loginform": login_form
        }

    return render(request, "cart/checkout.html", context)
