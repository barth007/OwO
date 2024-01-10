# CORE URL  MODULE

from django.urls import path
from core import views
from core import transfer

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("search-account/", transfer.search_users_account_number,
         name="search-account"),
    path("account-transfer/<account_number>", transfer.AmountTransfer,
         name="account-transfer"),
]