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


#################### settlement #######################
@login_required
def requestSettlement(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "account": account,
        "transaction": transaction
    }
    return render(request, "payment_request/settlement-confirmation.html", context)


@login_required
def settlement_processing(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        request_granter = request.user
        request_granter_account = request_granter.account

        if request.method == "POST":
            pin = request.POST.get("pin-number")
            if pin == request_granter_account.pin_number:
                if request_granter_account.account_balance <= 0 or request_granter_account.account_balance <= transaction.amount:
                    messages.warning(
                        request, "Insufficient Funds, Please Fund your account and try again later")
                else:
                    request_granter_account.account_balance -= transaction.amount
                    request_granter_account.save()
                    account.account_balance += transaction.amount
                    account.save()
                    transaction.status = "request_settled"
                    transaction.save()
                    messages.success(
                        request, f"Settlement to {account.user.kyc.full_name} was successfully")
                    return redirect("core:request-settlement-completed", account.account_number, transaction.transaction_id)
            else:
                messages.warning(request, "Incorrect pin")
                return redirect("core:request-confirmation", account.account_number, transaction.transaction_id)
    except Transaction.DoesNotExist:
        messages.warning(request, "Error occurred")
        return redirect("core:dashboard")


@login_required
def requestSettlementCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        messages.warning(request, "Error Occurred")
        return redirect("account:dashboard")
    context = {
        "account": account,
        "transaction": transaction
    }
    return render(request, "payment_request/request-settlement-granted.html", context)


@login_required
def deletePaymentRequest(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        user = request.user
        user_account = user.account
        if user == transaction.sender and user_account.account_number == account_number:
            transaction.delete()
            messages.success(request, "Payment Request Deleted successfully")
            return redirect("core:transactions")
    except Transaction.DoesNotExist:
        messages.warning(request, "Error Occurred")
        return redirect("acccount:dashboard")


@login_required
def cancelRecievedRequest(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        user = request.user
        user_account = user.account
        if user == transaction.reciever and user_account.account_number == account_number:
            transaction.status = "request_rejected"
            transaction.save()
            messages.error(request, "Request Rejected")
            return redirect("core:transactions")
    except Transaction.DoesNotExist:
        messages.warning(request, "Error Occurred")
        return redirect("account:dashboard")
