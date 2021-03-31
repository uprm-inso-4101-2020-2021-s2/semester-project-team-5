from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from items.models import Item
from .models import Cart, cart_item




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
    context = {
        "title": 'Cart',
        'cart_view': True,
    }
    if request.session.get('cart_id', None) is not None:
        cart_obj = Cart.objects.get(pk=request.session['cart_id'])
        request.session['cart_total'] = cart_obj.items.count()
        context.update({"cart": cart_obj})
    return render(request, "cart/main.html", context)


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
            if 'remove' in request.GET:
                cart_obj.cart_cart.get(cart_id=request.session['cart_id'], item_id=item_id).delete()
            else:
                query = cart_obj.cart_cart.get(cart_id=request.session['cart_id'], item_id=item_id)
                query.quantity = query.quantity + 1
                query.save()
        else:
            cart_obj.cart_cart.add(item_obj)
        request.session['cart_total'] = cart_obj.items.count()
    return redirect('cart:cart_home')

@require_http_methods(['PUT', 'GET'])
def checkout_home(request):
    if request.is_ajax():
        cart = Cart.objects.get(pk=request.session['cart_id'])
        cart.checkout = True
        cart.save()

        new_cart = Cart(user_id=request.user.pk)
        new_cart.save()
        request.session['cart_id'] = new_cart.pk
        return redirect('cart:cart_home')

    cart = Cart.objects.get(pk=request.session['cart_id'])
    context = {
        'cart': cart,
        'title': 'Checkout',
        'update_url': reverse('cart:checkout')
    }
    # if request.method == 'POST':

    return render(request, "cart/checkout.html", context)
    # if qs.count() == 1:
    #     cart_created = False
    #     cart_obj = qs.first()
    #     if request.user.is_authenticated and cart_obj.user is None:  # once it gets authenticated it changes to that user
    #         cart_obj.user = request.user
    #         cart_obj.save()
    # else:
    #     cart_obj = Cart.objects.new(user=request.user)
    #     cart_created = True
    #     request.session['cart_id'] = cart_obj.id
    # order_obj = None
    # if cart_created or cart_obj.items.count() == 0:
    #     return redirect('cart:cart_home')
    # else:
    #     order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    #     user = request.user
    #     # billing_profile =
    #     # login_form = LoginForm()
    #     # if user.is_authenticated:
    #     #     billing_profile = None
    #
    #     context = {
    #         "object": order_obj,
    #         "billing": billing_profile,
    #         "loginform": login_form
    #     }

    # return render(request, "cart/checkout.html", context)
