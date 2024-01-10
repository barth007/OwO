# module account views

from django.shortcuts import render, redirect
from account.models import Account, Kyc
from account.form import KycForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def account(request):
    if request.user.is_authenticated:

        try:
            kyc = Kyc.objects.get(user=request.user)
            account = Account.objects.get(user=request.user)
            context = {
                'kyc': kyc,
                'account': account
            }
            return render(request, 'account/account.html', context)
        except Kyc.DoesNotExist:
            account = Account.objects.get(user=request.user)
            context = {
                'account': account
            }
            messages.warning(request, 'You need to submit your kyc')
            return render(request, 'account/account.html', context)
    else:
        messages.warning(request, "you're not login")
        return redirect('user_auth:sign-in')


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
        if request.method == "POST":
            form = KycForm(request.POST, request.FILES)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = user
                new_form.account = account
                new_form.save()
                messages.success(
                    request, "Kyc successfully submitted, In review now")
                return redirect("account:account")
        else:
            form = KycForm(instance=kyc)
    context = {
        'account': account,
        'form': form,
        'kyc': kyc,
    }
    return render(request, 'account/kyc-form.html', context)

