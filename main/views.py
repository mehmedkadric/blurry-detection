from django.contrib.auth import login as django_login, authenticate, logout as django_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CustomUserChangeForm
import logging

logger = logging.getLogger('phd_logger')


# Create your views here.
def index(request):
    log_request(request, "home")
    context = {}
    return render(request, 'home.html', context=context)


def about(request):
    log_request(request, "about")
    return render(request, 'about.html')


def login(request):
    log_request(request, "login")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                messages.info(request, f"Welcome {user.first_name}!")
                return redirect("main:index")
            else:
                messages.error(request, "Invalid username or password")
                return redirect("main:login")
        else:
            errors = form.errors.as_data()
            for key in errors:
                for error in errors[key]:
                    messages.error(request, error.message)

            return redirect("main:login")
    if request.user.is_authenticated:
        messages.info(request, "Already logged in")
        return redirect("main:index")
    form = AuthenticationForm()

    context = {
        "form": form,
    }

    return render(request, "login.html", context=context)


def logout(request):
    log_request(request, "logout")
    django_logout(request)
    messages.info(request, "Logged out.")
    return redirect("main:index")


def register(request):
    log_request(request, "register")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            django_login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("main:index")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            redirect("main:register")

    form = UserRegistrationForm

    context = {
        "form": form,
    }

    return render(request, "register.html", context=context)


@login_required(login_url='/login')
def profile(request, user_id):
    user_info = User.objects.get(id=user_id)

    context = {
        'user': user_info,
    }
    return render(request=request, template_name="profile.html", context=context)


def log_request(request, view):
    if request.META.get('REMOTE_ADDR'):
        client_ip = request.META.get('REMOTE_ADDR')
    else:
        client_ip = 'AnonymousUser'
    logger.info(f"{view}. Method: {request.method} by {client_ip} ({request.user})")


@login_required(login_url='/login')
def update_user(request, user_id):
    log_request(request, "update_user")
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('main:profile', user_id=user_id)
        else:
            messages.error(request, form.errors.as_data())
    else:
        form = CustomUserChangeForm(instance=user)

    context = {
        'form': form,
        'user_id': user_id,
    }

    return render(request, 'profile_update.html', context=context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('main:change_password')
        else:
            messages.error(request, form.errors.as_data())
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})