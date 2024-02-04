from django.contrib import admin
from core.models import Transaction, CreditCard


class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'transaction_type',
                     'status', 'reciever', 'sender']
    list_display = ['user', 'amount', 'transaction_type',
                    'status', 'reciever', 'sender']


class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type']
    list_display = ['card_owner', 'amount', 'card_type']


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
