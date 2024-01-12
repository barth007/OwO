from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction
from decimal import Decimal


@login_required
def search_users_account_number(request):
    # account = Account.objects.get(user=request.user)
    account = Account.objects.all()
    query = request.POST.get("account_number")
    if query:
        account = account.filter(
            Q(account_number=query) |
            Q(account_id=query)
        ).distinct
    context = {
        "query": query,
        "account": account,
    }
    return render(request, "transfer/search-account.html", context)


@login_required
def AmountTransfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        messages.warning(request, "Account does not exist.")
        return redirect("core:search-account")

    context = {
        "account": account,
    }
    return render(request, "transfer/account-transfer.html", context)


@login_required
def amountTransferProcess(request, account_number):
    # get the receivers account  instance
    account = Account.objects.get(account_number=account_number)
    # get the logged in user making the request
    sender = request.user
    # get receiver
    reciever = account.user
    # the account sending the money from
    sender_account = request.user.account
    # the account number receiving the money
    reciever_account = account
    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")
        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                sender=sender,
                reciever=reciever,
                reciever_account=reciever_account,
                sender_account=sender_account,
                status="processing",
                transaction_type="transfer"
            )
            new_transaction.save()
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "Insufficient Fund")
            return redirect("core:account-transfer", account.account_number)
    else:
        messages.warning(request, "Error Occurred, please try again later")
        return redirect("account:account")


@login_required
def transactionConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        messages.warning(request, "transaction does not exit")
        return redirect("account:account")

    context = {
        "account": account,
        "transaction": transaction
    }
    return render(request, "transfer/transfer-confirmation.html", context)


@login_required
def transferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    # the account sending the money from
    sender_account = request.user.account
    # the account number receiving the money
    reciever_account = account
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()
            sender_account.account_balance -= transaction.amount
            sender_account.save()
            reciever_account.account_balance += transaction.amount
            reciever_account.save()
            messages.warning(request, "Transfer successful")
            return redirect("core:transfer-completed",  account.account_number, transaction_id)
        else:
            messages.warning(request, "Incorrect pin")
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "An Error occurred, try again later")
        return redirect("account:account")


@login_required
def TransferCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transfer does not exist.")
        return redirect("account:account")
    context = {
        "account": account,
        "transaction": transaction
    }
    return render(request, "transfer/transfer-completed.html", context)
