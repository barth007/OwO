# CORE URL  MODULE

from django.urls import path
from core import views
from core import transfer
from core import transaction

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("search-account/", transfer.search_users_account_number,
         name="search-account"),
    path("account-transfer/<account_number>", transfer.AmountTransfer,
         name="account-transfer"),
    path("account-transfer-process/<account_number>", transfer.amountTransferProcess,
         name="account-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/",
         transfer.transactionConfirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>/",
         transfer.transferProcess, name="transfer-process"),
    path("transfer-completed/<account_number>/<transaction_id>/", transfer.TransferCompleted,
         name="transfer-completed"),

    # transaction
    path("transactions/",
         transaction.transaction_list, name="transactions"),
]
