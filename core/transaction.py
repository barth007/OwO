from django.shortcuts import render, redirect
from core.models import Transaction
from account.models import Account
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def transaction_list(request):
    sender_transaction = Transaction.objects.filter(
        sender=request.user).order_by("-id")
    receiver_transaction = Transaction.objects.filter(
        sender=request.user).order_by("-id")

    context = {
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction
    }
    return render(request, "transaction/transaction-list.html", context)
