from django.shortcuts import render, redirect
from items.models import Item
from .models import Cart


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

    items = cart_obj.items.all()
    total = 0
    for eachitem in items:
        total += eachitem.price
    cart_obj.total = total
    cart_obj.save()
    return render(request, "cart/main.html", {})


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
    return redirect('cart:cart_home')
