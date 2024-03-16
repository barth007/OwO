# CORE URL  MODULE

from django.urls import path
from core import views
from core import transfer, transaction, payment_request, credit_card
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
    path("transaction_detail/<transaction_id>/",
         transaction.transaction_Detail, name="transaction_detail"),

    # payment request
    path("request-search-user/", payment_request.searchUserRequest,
         name="request-search-user"),
    path("amount-request/<account_number>/", payment_request.amountRequest,
         name="amount-request"),
    path("amount-request-process/<account_number>/", payment_request.amountRequestProcess,
         name="amount-request-process"),
    path("amount-request-confirmation/<account_number>/<transaction_id>/", payment_request.amountRequestConfirmation,
         name="amount-request-confirmation"),
    path("amount-request-final-process/<account_number>/<transaction_id>/", payment_request.amountRequestFinalprocess,
         name="amount-request-final-process"),
    path("request-completed/<account_number>/<transaction_id>/", payment_request.requestCompleted,
         name="request-completed"),
    path("request-confirmation/<account_number>/<transaction_id>/", payment_request.requestSettlement,
         name="request-confirmation"),
    path("request-settlement-process/<account_number>/<transaction_id>/", payment_request.settlement_processing,
         name="request-settlement-process"),
    path("request-settlement-completed/<account_number>/<transaction_id>/", payment_request.requestSettlementCompleted,
         name="request-settlement-completed"),
    path("delete-request/<account_number>/<transaction_id>/", payment_request.deletePaymentRequest,
         name="delete-request"),
    path("cancel-request/<account_number>/<transaction_id>/", payment_request.cancelRecievedRequest,
         name="cancel-request"),

    # credit card url
    path("card/<card_id>",
         credit_card.card_detail, name="card_details"),
    path("funding/<card_id>",
         credit_card.card_funding, name="funding"),
    path("withdrawal/<card_id>",
         credit_card.card_withdrawer, name="withdrawer"),
    path("delete_card/<card_id>",
         credit_card.delete_user_card, name="delete_card"),
]
