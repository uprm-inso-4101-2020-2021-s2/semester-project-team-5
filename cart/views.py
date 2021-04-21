import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from items.models import Item
from .models import Cart, CartItem


def get_or_update_cart(request, user):
    cart_obj = None
    qs = Cart.objects.filter(user_id=user.pk, checkout=False)
    if qs.exists():
        cart_obj = qs.last()
        if request.session.get('cart_id', None) is not None:
            user_cart_item_list = CartItem.objects.filter(cart_id=cart_obj.pk).values_list('item_id', flat=True)
            for item_cart in CartItem.objects.filter(cart_id=request.session['cart_id']):
                if item_cart.item_id in user_cart_item_list:
                    updated_item = CartItem.objects.get(cart_id=cart_obj.pk, item_id=item_cart.item_id)
                    updated_item.quantity = item_cart.quantity + updated_item.quantity
                    updated_item.save()
                else:
                    added_item = CartItem(cart_id=cart_obj.pk, item_id=item_cart.item_id)
                    added_item.quantity = item_cart.quantity
                    added_item.save()

            session_cart = Cart.objects.get(pk=request.session['cart_id'])
            session_cart.delete()

    elif request.session.get('cart_id', None) is not None:
        cart_obj = Cart.objects.get(pk=request.session['cart_id'])
        if cart_obj.user is None:
            cart_obj.user_id = user.pk
            cart_obj.save()

    if cart_obj is None:
        cart_obj = Cart.objects.new(user)

    return cart_obj


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
            add_item = CartItem(cart_id=request.session['cart_id'], item_id=item_id)
            add_item.save()
        cart_obj.update_total()
        request.session['cart_total'] = cart_obj.items.count()
    return redirect('cart:cart_home')


@login_required(login_url='/users/login/')
@require_http_methods(['PUT', 'GET'])
def checkout_home(request):
    if request.is_ajax():
        cart = Cart.objects.get(pk=request.session['cart_id'])
        for obj in cart.cart_cart.all():
            obj.item.quantity = obj.item.quantity - obj.quantity
            obj.item.save()
        cart.checkout = True
        cart.updated = datetime.datetime.now()
        cart.save()
        new_cart = Cart(user_id=request.user.pk)
        new_cart.save()
        request.session['cart_id'] = new_cart.pk
        return HttpResponse(status=200)

    cart = Cart.objects.get(pk=request.session['cart_id'])
    context = {
        'cart': cart,
        'title': 'Checkout',
        'checkout': True
    }
    return render(request, "cart/checkout.html", context)


@login_required(login_url='/users/login/')
def orders(request):
    order_list = Cart.objects.filter(user_id=request.user.pk, checkout=True).order_by('-updated')
    context = {
        'order_list': order_list,
    }
    return render(request, "cart/orders_list.html", context)


@login_required(login_url='/users/login/')
def orders_details(request, cart_id):
    order = get_object_or_404(Cart, pk=cart_id)
    context = {
        'readonly': True,
        'title': 'Order {id} - {date}'.format(id=cart_id, date=order.updated.strftime('%m/%d/%Y')),
        'cart': order,
    }
    return render(request, "cart/main.html", context)


@require_http_methods(['GET'])
@login_required(login_url='/users/login/')
def sells_activity(request):
    context = {}
    items = []
    carts_ids = Cart.objects.filter(checkout=True, cart_cart__item__owner_id=request.user.pk).values_list('pk', flat=True)
    cart = CartItem.objects.filter(cart_id__in=carts_ids, item__owner_id=request.user.pk)
    for cart_items in cart.all():
        items.append((
            cart_items.item.images.first().source.url,
            cart_items.item.name,
            cart_items.quantity,
            cart_items.cart.user,
            cart_items.cart.user.email,
            cart_items.cart.user.phone,
            cart_items.cart.user.locations.last(),
        ))

    context.update({'items': items, 'title': 'Orders List'})
    return render(request, 'cart/sales_list.html', context=context)