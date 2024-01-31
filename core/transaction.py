from django.shortcuts import render, redirect
from core.models import Transaction
from account.models import Account, Kyc
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def transaction_list(request):
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        try:
            kyc = Kyc.objects.get(user=request.user)
        except Kyc.DoesNotExist:
            messages.warning(request, "submit your kyc.")
            return redirect("user_auth:sign-in")
        sender_transaction = Transaction.objects.filter(
            sender=request.user, transaction_type="transfer").order_by("-id")
        receiver_transaction = Transaction.objects.filter(
            reciever=request.user, transaction_type="transfer").order_by("-id")
        request_sender_tranx = Transaction.objects.filter(
            sender=request.user, transaction_type="payment_request"
        ).order_by("-id")
        request_reciever_tranx = Transaction.objects.filter(
            reciever=request.user, transaction_type="payment_request"
        ).order_by("-id")
    else:
        messages.warning(request, "login required.")
        return redirect("user_auth:sign-in")

    context = {
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction,
        "request_sender_tranx": request_sender_tranx,
        "request_recieve_tranx": request_reciever_tranx,
        "account": account,
        "kyc": kyc
    }
    return render(request, "transaction/transaction-list.html", context)


@login_required
def transaction_Detail(request, transaction_id):
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        try:
            kyc = Kyc.objects.get(user=request.user)
        except Kyc.DoesNotExist:
            messages.warning(request, "submit your kyc.")
            return redirect("user_auth:sign-in")
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    else:
        messages.warning(request, "login required.")
        return redirect("user_auth:sign-in")

    context = {
        "transaction": transaction,
        "account": account,
        "kyc": kyc
    }
    return render(request, "transaction/transaction-detail.html", context)
