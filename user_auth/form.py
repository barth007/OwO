# USER AUTH FORM MODULE

from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_auth.models import User

class UserRegisterForm(UserCreationForm):
    """This form will create fields for new users"""

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
    