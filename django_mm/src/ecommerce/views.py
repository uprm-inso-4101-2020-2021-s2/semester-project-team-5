from django.shortcuts import render
from items.models import Item


def home_page(request):
    items = Item.objects.all()
    context = {
        "members": "STEPH WALLY MANNY HEC CORA ANGEL",
        "content": "Best Puerto rican ecommerce site",
        "items": items

    }
    if request.user.is_authenticated:
        context["premium_content"] = "YOU DA BEST!"
    return render(request, "homePage.html", context)
