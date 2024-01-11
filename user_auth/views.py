# USER AUTH VIEW MODULE

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user_auth.form import UserRegisterForm, UserLoginForm

def index(request):
    
    return render(request, 'auth/sign-in.html')

def register_view (request):
    """
    registration of a new user
    """

    form = UserRegisterForm()
    print(request.method)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f"Hi {username} your account has been created successfully"
            )
            # users should login after registration
            new_user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('account:account')
    elif request.user.is_authenticated:
        messages.warning(request, f"You're already logged in")
    context = {
        'form': form
        }
    return render(request, 'auth/sign-up.html', context)

def login_view(request):
    """ This will login users"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            messages.success(request, f"{logged_user} is logged in")
            logged_user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if logged_user is not None:
                login(request, logged_user)
                return redirect('account:account')
            else:
                messages.warning(request, f"Invalid login credentials")
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