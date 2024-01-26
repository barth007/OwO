from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction
from decimal import Decimal


@login_required
def searchUserRequest(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")
    if query:
        account = account.filter(
            Q(account_number=query)
        )
    context = {
        "account": account,
        "query": query
    }
    return render(request, "payment_request/payment_request.html", context)


@login_required
def amountRequest(request, account_number):
    account = Account.objects.get(account_number=account_number)
    context = {
        "account": account
    }
    return render(request, "payment_request/amount-request.html", context)


@login_required
def amountRequestProcess(request, account_number):
    account = Account.objects.get(account_number=account_number)
    sender = request.user
    reciever = account.user
    sender_account = request.user.account
    reciever_account = account
    if request.method == "POST":
        amount_request = request.POST.get("amount-request")
        description = request.POST.get("description")
        amount = Decimal(amount_request)
        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            sender=sender,
            reciever=reciever,
            reciever_account=reciever_account,
            sender_account=sender_account,
            status="request_processing",
            transaction_type="payment_request",
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "Error occurred, please try again")
        return redirect("account:dashboard")


@login_required
def amountRequestConfirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "account": account,
        "transaction": transaction
    }
    return render(request, "payment_request/amount-request-confirmation.html", context)


@login_required
def amountRequestFinalprocess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    if request.method == "POST":
        pin = request.POST.get("pin-number")
        if request.user.account.pin_number == pin:
            transaction.status = "request_sent"
            transaction.save()
            messages.success(request, "Your payment request was successful")
            return redirect("core:request-completed", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "Error occurred, try again later!")
        return redirect("account:dashboard")


@login_required
def requestCompleted(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        "transaction": transaction
    }
    return render(request, "payment_request/request-completed.html", context)
