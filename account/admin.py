from django.contrib import admin
from account.models import Account, Kyc
from user_auth.models import User
from import_export.admin import ImportExportModelAdmin


class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'account_balance']
    list_display = ['user', 'account_number', 'account_status', 'account_balance']
    list_filter = ['account_status']


class KycAdminModel(ImportExportModelAdmin):
    search_fields = ["full_name"]
    list_display = ['user', 'full_name']


admin.site.register(Account, AccountAdminModel)
admin.site.register(Kyc, KycAdminModel)
