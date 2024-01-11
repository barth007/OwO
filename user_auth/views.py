# USER AUTH VIEW MODULE

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user_auth.form import UserRegisterForm, UserLoginForm
from user_auth.models import User


def register_view(request):
    """
    Registration of a new user
    """
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print(form)
            # Check if email or phone number already exists
            email_exists = User.objects.filter(
                email=form.cleaned_data['email']).exists()
            phone_exists = User.objects.filter(
                phone_number=form.cleaned_data['phone_number']).exists()

            if email_exists:
                messages.error(request, 'This email is already registered.')
            elif phone_exists:
                messages.error(
                    request, 'This phone number is already registered.')
            else:
                # Neither email nor phone number exists, proceed with registration
                new_user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(
                    request,
                    f"Hi {username}, your account has been created successfully."
                )
                # Users should login after registration
                new_user = authenticate(
                    # Use email as the username for authentication
                    username=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )
                login(request, new_user)
                return redirect('account:kyc-form')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    elif request.user.is_authenticated:
        messages.warning(request, "You're already logged in.")

    context = {'form': form}
    return render(request, 'auth/sign-up.html', context)


def login_view(request):
    """ This will login users"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print(form.data)
        if form.is_valid():
            print("is okay")
            print(f"Username: {form.cleaned_data['email']}")
            logged_user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if logged_user is not None:
                login(request, logged_user)
                messages.success(request, f"{logged_user} is logged in")
                return redirect('account:account')
            else:
                messages.warning(request, f"Invalid login credentials")
        else:
            print(form.errors)
            print("not okay")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    elif request.user.is_authenticated:
        messages.warning(request, f"You're already logged in")
        return redirect('account:account')

    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'auth/sign-in.html', context)


def logout_view(request):
    """ log users out"""

    logout(request)
    messages.success(request, f"You're logged out")
    return redirect('user_auth:sign-in')
