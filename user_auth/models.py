from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from typing import Dict, List


HELP_TEXT_AND_VERBOSE_NAME: Dict[str, Dict[str, List[str]]] ={
    'user': {
        'username': ['Enter User Name', 'User Name'],
        'email': ['Enter a valid email address', 'Email Address'],
        'phone_number': ['+2348121277476', 'Phone Numer'],
        'is_staff': ['A staff', 'staff']
    }
}

class User (AbstractUser):
    (
        username_,
        email_,
        phone_number_,
        is_staff_,
    )= HELP_TEXT_AND_VERBOSE_NAME["user"].values()
    username = models.CharField(
        max_length=50,
        help_text=username_[0],
        verbose_name=username_[1],
    )
    email = models.EmailField(
        max_length=200,
        unique=True,
        help_text=email_[0],
        verbose_name=email_[1],
    )
    phone_number = PhoneNumberField(
        unique=True,
        help_text=phone_number_[0],
        verbose_name=phone_number_[1],
    )
    is_staff = models.BooleanField(
        help_text=is_staff_[0],
        verbose_name=is_staff_[1],
    )

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username', 'phone_number']

    def __str__(self):
        return self.username