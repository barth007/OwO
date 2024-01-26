from django.contrib import admin
from core.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'transaction_type',
                     'status', 'reciever', 'sender']
    list_display = ['user', 'amount', 'transaction_type',
                    'status', 'reciever', 'sender']


admin.site.register(Transaction, TransactionAdmin)
