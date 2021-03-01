from django.shortcuts import render


def home_page(request):
    context = {
        "members": "STEPH WALLY MANNY HEC CORA ANGEL",
        "content": "Best Puerto rican ecommerce site",

    }
    if request.user.is_authenticated:
        context["premium_content"] = "YOU DA BEST!"
    return render(request, "homePage.html", context)