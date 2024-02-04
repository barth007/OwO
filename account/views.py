# module account views

from django.shortcuts import render, redirect
from account.models import Account, Kyc
from core.models import Transaction
from account.form import KycForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from core.form import CreditCardForm
from core.models import CreditCard


@login_required
def account(request):
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        try:
            kyc = Kyc.objects.get(user=request.user)
        except Kyc.DoesNotExist:
            messages.warning(request, 'You need to submit your kyc')
            return redirect("account:kyc-form")
    else:
        messages.warning(request, "you're not logged in")
        return redirect('user_auth:sign-in')
    context = {
        'kyc': kyc,
        'account': account
    }
    return render(request, 'account/account.html', context)


@login_required
def kyc_registration_view(request):
    user = request.user
    account = get_object_or_404(Account, user=user)

    try:
        kyc = Kyc.objects.get(user=user)
        form = KycForm(request.POST or None,
                       request.FILES or None, instance=kyc)
    except Kyc.DoesNotExist:
        kyc = None

        form = KycForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.account = account

            new_form.user = user
            new_form.save()
            account.account_status = "active"
            account.account_balance = 2000.00
            account.save()
            messages.success(
                request, "Kyc successfully submitted and you're credited with $2000 reward.")
            return redirect("account:account")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    context = {'account': account, 'form': form, 'kyc': kyc}
    return render(request, 'account/kyc-form.html', context)


@login_required
def dashboard(request):
    if request.user.is_authenticated:

        try:
            kyc = Kyc.objects.get(user=request.user)
            account = Account.objects.get(user=request.user)
            credit_card = CreditCard.objects.filter(
                card_owner=request.user).order_by("-id")
            sender_transaction = Transaction.objects.filter(
                sender=request.user, transaction_type="transfer").order_by("-id")
            receiver_transaction = Transaction.objects.filter(
                reciever=request.user, transaction_type="transfer").order_by("-id")

        except Kyc.DoesNotExist:
            messages.warning(request, "you need to submit kyc.")
            return redirect("account:kyc-form")
        sender_transaction = Transaction.objects.filter(
            sender=request.user, transaction_type="transfer").order_by("-id")
        receiver_transaction = Transaction.objects.filter(
            reciever=request.user, transaction_type="transfer").order_by("-id")
        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.card_owner = request.user
                new_form.save()
                card_id = new_form.card_id
                messages.success(request, "Card Successfully Added")
                return redirect("account:dashboard")
        else:
            form = CreditCardForm()
    else:
        messages.warning(request,  "You're not logged in.")
        return redirect("user_auth:sigin-in")
    context = {
        "kyc": kyc,
        "account": account,
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction,
        "form": form,
        "credit_card": credit_card
    }
    return render(request, "account/dashboard.html", context)
