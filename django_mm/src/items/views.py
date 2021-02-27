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


def item_list_view(request):
    queryset = Item.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "items/item_list.html", context)


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    temp_name = "items/item_detail.html"

    # TEST TO SEE ITEMS INFORMATION
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context


def item_detail_view(request, pk=None, *args, **kwargs):

    selected_item = get_object_or_404(Item, pk=pk)
    context = {
        'object_list': selected_item
    }
    return render(request, "items/item_detail.html", context)
