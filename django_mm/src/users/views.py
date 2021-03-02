from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model

from .models import Location

User = get_user_model()


@require_http_methods(['POST', 'GET'])
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


@require_http_methods(['POST', 'GET'])
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username=username, email=email, password=password)

        new_user.first_name = form.cleaned_data.get('first_name')
        new_user.last_name = form.cleaned_data.get('last_name')
        new_user.phone = form.cleaned_data.get('phone')
        new_user.save()

        location = Location.objects.create(user_id=new_user.pk, address=form.cleaned_data.get('address'),
                                           city=form.cleaned_data.get('city'), zip_code=form.cleaned_data.get('zip_code'))
        location.save()
        messages.success(request, 'User "%s" added succesfully' % new_user.username)

    return render(request, "authentication/register.html", context)