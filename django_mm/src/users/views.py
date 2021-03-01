from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()


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
        new_user = User.objects.create(username=username, email=email, password=password)
        print(new_user)
    return render(request, "authentication/register.html", context)