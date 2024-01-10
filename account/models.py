# account models

from sqlite3 import IntegrityError
from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from user_auth.models import User
from django.db.models.signals import post_save
from django.contrib import messages


# multiple choice
ACCOUNT_STATUS = (
    ("active", "Active"),
    ("in-active", "In-active")
)

GENDER = (
    ("default", "Select"),
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)

MARITAL_STATUS = (
    ("single", "Single"),
    ("married", "Married"),
    ("divorce", "Divorce"),
)
IDENTITY_TYPE = (
    ("national_id", "National Identity Card"),
    ("driver licence", "Driver Licence"),
    ("int'l passport", "International Passport"),
)


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return f"user_{instance.user.id}/{filename}"


class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(
        length=10, max_length=25, prefix="217", alphabet="123456789")
    account_id = ShortUUIDField(
        unique=True, length=7, max_length=25, prefix="DEX", alphabet="123456789")
    pin_number = ShortUUIDField(
        unique=True, length=4, max_length=7, prefix="217", alphabet="123456789")
    ref_code = ShortUUIDField(unique=True, length=10,
                              max_length=25, alphabet="abcdefgh123456789")
    account_status = models.CharField(
        max_length=100, choices=ACCOUNT_STATUS, default="in-active")
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='recommended_by')

    class Meta:
        ordering = ['date']

    def __str__(self):
        try:
            return f"{self.user}"
        except:
            return "Account Models"


class Kyc(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="kyc", default="default.jpg")
    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=40, default="default")
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=40)
    identity_image = models.ImageField(
        upload_to="kyc", null=False, blank=False, default=None)
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc")

    # addresss
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # contact
    mobile = models.CharField(max_length=1000)
    fax = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


# receiver signals
def create_account(sender, instance, created, **kwargs):
    try:
        if created:
            Account.objects.create(user=instance)
    except IntegrityError as e:
        print(f"Integrity Error occur: {e}")


def save_account(sender, instance, **kwargs):
    try:
        instance.account.save()
    except IntegrityError as e:
        print(f"Integrity Error occur: {e}")


#  sender signals
post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)

