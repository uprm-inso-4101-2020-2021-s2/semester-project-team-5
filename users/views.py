from django.contrib import messages

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from cart.views import get_or_update_cart
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import auth
from .models import Location

User = get_user_model()


@require_http_methods(['POST', 'GET'])
def login_page(request, backend=None):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            cart_obj = get_or_update_cart(request, user)
            request.session['cart_total'] = cart_obj.items.count()
            request.session['cart_id'] = cart_obj.id
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect("/")
        else:
            context.update({'error': 'Invalid credentials.'})
    return render(request, "authentication/login.html", context)


def create_or_update_user(form, user=None):
    if not user:
        user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                        email=form.cleaned_data.get('email'),
                                        password=form.cleaned_data.get('password'))
        Location.objects.create(user_id=user.pk).save()
    else:
        user.email = form.cleaned_data.get('email')
        if (form.cleaned_data.get('password') is not None) and \
                (form.cleaned_data.get('password') != ''):
            user.set_password(form.cleaned_data.get('password'))

    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.phone = form.cleaned_data.get('phone')
    user.save()

    location = user.locations.last()
    location.address = form.cleaned_data.get('address')
    location.city = form.cleaned_data.get('city')
    location.zip_code = form.cleaned_data.get('zip_code')
    location.save()
    return user


@require_http_methods(['POST', 'GET'])
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'page_name': 'Create account',
        'form': form,
        'button_text': 'Register'
    }
    if form.is_valid():
        new_user = create_or_update_user(form)
        login(request, new_user)
        cart_obj = get_or_update_cart(request, new_user)
        request.session['cart_total'] = cart_obj.items.count()
        request.session['cart_id'] = cart_obj.id
        return HttpResponseRedirect("/")

    return render(request, "authentication/user_information.html", context)


def logout_page(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url='/users/login/')
@require_http_methods(['POST', 'GET'])
def user_profile_page(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    form = ProfileForm(request, request.POST or None, instance=user)
    context = {
        'page_name': 'Profile',
        'form': form,
        'button_text': 'Submit change'
    }
    if request.method == 'POST' and form.is_valid():
        create_or_update_user(form, user)
        messages.success(request, 'User profile updated successfully')
    return render(request, "authentication/user_information.html", context)

