from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def home_page(request):
    context = {
        "members": "STEPH WALLY MANNY HEC CORA ANGEL",
        "content": "Best Puerto rican ecommerce site",

    }
    if request.user.is_authenticated:
        context["premium_content"] = "YOU DA BEST!"
    return render(request, "homePage.html", context)


def login_page(request, backend=None):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    # print(request.user.is_authenticated)
    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # print(request.user.is_authenticated)
            login(request, user)
            # Redirect to a success page.
            context['form'] = LoginForm()
            if user.is_superuser:
                return redirect("/admin")
            else:
                return redirect("/")
        else:
            # Return an 'invalid login' error message.
            print("Error couldn't log in")
    return render(request, "authentication/login.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    # print(request.user.is_authenticated)
    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "authentication/register.html", context)
