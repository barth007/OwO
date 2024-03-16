
from django.shortcuts import render, redirect
from account.models import Account, Kyc
from core.models import Transaction
from account.form import KycForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from decimal import Decimal


@login_required
def card_detail(request, card_id):
    try:
        card = CreditCard.objects.get(card_id=card_id, card_owner=request.user)
        account = Account.objects.get(user=request.user)
        kyc = Kyc.objects.get(user=request.user)
    except CreditCard.DoesNotExist:
        messages.warning(request, "Error occurred, please try again")
        return redirect("account:dashboard")
    context = {
        "credit_card": card,
        "account": account,
        "kyc": kyc
    }
    return render(request, "credit_card/credit_card-details.html", context)


@login_required
def card_funding(request, card_id):
    try:
        card = CreditCard.objects.get(card_id=card_id, card_owner=request.user)
        account = Account.objects.get(user=request.user)
        if account.user == card.card_owner:
            if request.method == "POST":
                amount = request.POST.get("funding_amount")
                amount_dec = Decimal(amount)
                if amount_dec <= account.account_balance:
                    card.amount += amount_dec
                    account.account_balance -= amount_dec
                    card.save()
                    account.save()
                    messages.success(request, "Funded Card Successfully!")
                    return redirect("core:card_details", card.card_id)
                else:
                    messages.warning(request, "Insufficient Funds")
                    return redirect("account:dashboard")
    except CreditCard.DoesNotExist:
        messages.warning(request, "Error occurred")
        return redirect("account:dashboard")


@login_required
def card_withdrawer(request, card_id):
    try:
        card = CreditCard.objects.get(card_id=card_id, card_owner=request.user)
        account = Account.objects.get(user=request.user)
        if account.user == card.card_owner:
            amount = request.POST.get("amount")
            amount_dec = Decimal(amount)
            if amount_dec <= card.amount:
                card.amount -= amount_dec
                account.account_balance += amount_dec
                card.save()
                account.save()
                messages.success(request, "Withdrawal Successfull")
                return redirect("core:card_details", card.card_id)
            else:
                messages.warning(request, "Insufficent Fund")
                return redirect("core:card_details", card.card_id)
    except CreditCard.DoesNotExist:
        messages.warning(request, "Error Occured")
        return redirect("account:dashboard")


@login_required
def delete_user_card(request, card_id):
    try:
        card = CreditCard.objects.get(card_id=card_id, card_owner=request.user)
        account = Account.objects.get(user=request.user)
        if card.amount >= 0:
            account.account_balance += card.amount
            account.save()
            card.delete()
            messages.success(request, "Card Deleted Successfully!")
            return redirect("core:card_details", card.card_id)
    except CreditCard.DoesNotExist:
        messages.warning(request, "Error Occured")
        return redirect("account:dashboard")
