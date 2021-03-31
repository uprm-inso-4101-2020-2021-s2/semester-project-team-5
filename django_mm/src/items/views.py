from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from .forms import AddItemForm
from .models import Item, Image, CATEGORY
from cart.models import Cart


class SearchItemListView(ListView):
    template_name = "Items/searches.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchItemListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        items_dict = request.GET
        query = items_dict.get('q')
        if query is not None:
            return Item.objects.search(query)
        return Item.objects.none()


def item_list(request):
    queryset = Item.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "Items/item_list.html", context)


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    template_name = "Items/item_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        # cart_obj = Cart.objects.get(pk=self.request.session['cart_id'])
        # context['cart'] = cart_obj
        return context

    # Manage multiple slugs items
    def get_object(self, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        try:
            instance = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise Http404("Not found ...")
        return instance


def details(request, item_id=None):
    instance = Item.objects.get(pk=item_id)
    if instance is None:
        raise Http404("Product doesn't exist")

    context = {
        'item': instance
    }

    return render(request, "Items/item_detail.html", context)


@login_required(login_url='/users/login/')
@require_http_methods(['POST', 'GET'])
def add_item(request):
    form = AddItemForm(request.POST or None, request.FILES)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            item = Item(owner_id=request.user.id,
                        name=form.cleaned_data['name'],
                        description=form.cleaned_data['description'],
                        price=form.cleaned_data['price'],
                        quantity=form.cleaned_data['quantity'],
                        category=form.cleaned_data['category'])
            item.save()

            images = request.FILES.getlist('images')
            for image in images:
                image = Image(item_id=item.id, source=image)
                image.save()

    context = {
        'form': form,
    }
    return render(request, "Items/add_item.html", context)


@login_required(login_url='/users/login/')
@require_http_methods(['GET'])
def selling_items(request):
    queryset = Item.objects.filter(owner_id=request.user.pk)
    context = {
        'object_list': queryset,
        'title': "Selling items by {username}".format(username=request.user.username)
    }
    return render(request, "Items/item_list.html", context)


@require_http_methods(['GET'])
def search_item_by_category(request, category):
    queryset = Item.objects.filter(category=category)
    context = {
        'object_list': queryset,
        'title': CATEGORY[str(category)],
    }
    return render(request, "Items/item_list.html", context)


@login_required(login_url='/users/login/')
@require_http_methods(['POST', 'GET'])
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item_name = item.name
    if request.user.id == item.owner_id:
        item.delete()
        messages.success(request, 'Item {name} deleted successfully'.format(name=item_name))
        return HttpResponseRedirect(reverse('items:selling_items'))

    messages.error(request, 'Invalid request'.format(name=item_name))
    return HttpResponseRedirect(reverse('items:selling', args=(request.user.id,)), status=403) #must redirect to the change view of the item



