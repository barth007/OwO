# USER AUTH ADMIN MODULE

from django.contrib import admin
from user_auth.models import User
from user_auth.kyc_models import KYC

admin.site.register(User)
admin.site.register(KYC)