# USER AUTH FORM MODULE

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from user_auth.models import User

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    """This form will create fields for new users"""

    class Meta:
        model = User
        fields = ['username', 'email',
                  'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].help_text
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].help_text
        self.fields['phone_number'].widget.attrs['placeholder'] = self.fields['phone_number'].help_text
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class UserLoginForm(AuthenticationForm):
    """This form will create fields to login users"""

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password'
