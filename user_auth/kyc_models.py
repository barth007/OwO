

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from typing import List, Dict

HELP_TEXT_AND_VERBOSE_NAME: Dict[str, Dict[str, List[str]]] ={
    'kyc': {
        'next_of_kin': ['Enter your next of kin Name', 'Next of Kin Name'],
        'nok_phone_number': ['+2348121277476', 'Next of Kin Phone Numer'],
        'bvn': ['Enter a valid bvn number', 'Bank verification Number'],
        'residential_address': ['Enter full residential address', 'Residential Address'],
        'sex': ['Select your gender', 'Sex'],
        'means_of_identification': ['Select a valid means of Identification', 'Bank verification Number'],
        'picture_upload': ['Upload a picture the selected means of Identification', 'ID card Image'],
        'phone_number': ['+2348121277476', 'Phone Number'],
    }
}


User = get_user_model()

class KYC(models.Model):
    # Define choices for means_of_identification field
    MEANS_OF_IDENTIFICATION_CHOICES = [
        ('nin', 'National Identification Number (NIN)'),
        ('passport', 'International Passport'),
        ('voters_card', 'Voter\'s Card'),
        ('drivers_license', 'Driver\'s License'),
    ]

    (
        next_of_kin_,
        nok_phone_number_,
        bvn_,
        residential_address_,
        sex_,
        means_of_identification_,
        picture_upload_,
        phone_number_,
    ) = HELP_TEXT_AND_VERBOSE_NAME["kyc"].values()

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kyc')
    next_of_kin = models.CharField(max_length=255, help_text=next_of_kin_[0], verbose_name=next_of_kin_[1])
    nok_phone_number = PhoneNumberField(
        unique=False,
        blank=False, 
        help_text=nok_phone_number_[0],
        verbose_name=nok_phone_number_[1],
    )
    bvn = models.CharField(max_length=11, unique=True, blank=False, help_text=bvn_[0], verbose_name=bvn_[1])
    residential_address = models.TextField(blank=False, help_text=residential_address_[0], verbose_name=residential_address_[1])
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=False, help_text=sex_[0], verbose_name=sex_[1])
    means_of_identification = models.CharField(max_length=20, choices=MEANS_OF_IDENTIFICATION_CHOICES, blank=False, help_text=means_of_identification_[0], verbose_name=means_of_identification_[1])
    picture_upload = models.ImageField(upload_to='kyc_pictures/', blank=False, null=False, help_text=picture_upload_[0], verbose_name=bvn_[1])
    phone_number = PhoneNumberField(
        unique=False,
        blank=False, 
        help_text=phone_number_[0],
        verbose_name=phone_number_[1],
    )
    is_verified = models.BooleanField(default=False)

    def clean(self):
        # Check if BVN consists only of digits
        if not self.bvn.isdigit():
            raise ValidationError("BVN must contain only digits.")

        # Check if BVN is exactly 11 characters
        if len(self.bvn) != 11:
            raise ValidationError("BVN must be exactly 11 characters.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation before saving
        super().save(*args, **kwargs)


    def __str__(self):
        return f'KYC for {self.user.username}'
