from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Item
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
        cart_id = self.request.session.get("cart_id", None)
        qs = Cart.objects.filter(id=cart_id)
        if qs.count() == 1:
            print("Cart ID exists")
            cart_obj = qs.first()
            if self.request.user.is_authenticated and cart_obj.user is None:  # once it gets authenticated it changes to that user
                cart_obj.user = self.request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=self.request.user)
            self.request.session['cart_id'] = cart_obj.id
        context['cart'] = cart_obj
        return context

    # Manage multiple slugs items
    def get_object(self, *args, **kwargs):
        Category = self.kwargs.get('Category')
        try:
            instance = Item.objects.get(Category=Category)
        except Item.DoesNotExist:
            raise Http404("Not found ...")
        except Item.MultipleObjectsReturned:
            qs = Item.objects.filter(Category=Category)
            return qs.first()
        except:
            raise Http404("No items")
        return instance
    # TEST TO SEE ITEMS INFORMATION
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context


def details(request, item_id=None):

    instance = Item.objects.get_by_id(item_id)
    if instance is None:
        raise Http404("Product doesn't exist")

    context = {
        'item': instance
    }

    return render(request, "Items/item_detail.html", context)
