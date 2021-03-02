from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Item


class ItemListView(ListView):
    queryset = Item.objects.all()
    temp_name = "items/item_list.html"

    # TEST TO SEE THE ITEMS INFORMATION
    # every class list view needs this method, to view the data
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ItemListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context


def item_list(request):
    queryset = Item.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "items/item_list.html", context)


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    temp_name = "items/item_detail.html"

    # Manage multiple slugs items
    def get_object(self, *args, **kwargs):
        request = self.request
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
    # selected_item = get_object_or_404(Item, pk=item_id)
    instance = Item.objects.get_by_id(item_id)
    if instance is None:
        raise Http404("Product doesn't exist")

    context = {
        # 'item': selected_item
        'item': instance
    }

    return render(request, "items/item_detail.html", context)
