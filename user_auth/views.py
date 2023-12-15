# USER AUTH VIEW MODULE

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user_auth.form import UserRegisterForm

def register_view (request):
    """
    registration of a new user
    """

    form = UserRegisterForm()
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
            login(
                request,
                new_user
            )
            return redirect('core:index')
    elif request.user.is_authenticated:
        messages.warning(
            request,
            f"You're already logged in"
        )
    context = {
        'form': form
    }
    return render(request, 'auth/sign-up.html', context)