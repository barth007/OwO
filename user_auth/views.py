# USER AUTH VIEW MODULE

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user_auth.form import UserCreationForm
from django.contrib import messages

def register_view (request):
    """
    registration of a new user
    """

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = new_user.cleaned_data.get('username')
            messages.success(
                request,
                f"Hi {username} your account has been created successfully"
            )
            # users should login after registration
            authenticate(
                username=new_user.cleaned_data['email'],
                password=new_user.cleaned_data['password1']
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