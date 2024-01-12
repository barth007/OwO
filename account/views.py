# module account views

from django.shortcuts import render, redirect
from account.models import Account, Kyc
from core.models import Transaction
from account.form import KycForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


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


# @login_required
# def kyc_registration_view(request):
#     user = request.user
#     print(user)
#     print(request.method)
#     print(request.path)

#     if request.method == "POST":
#         form = KycForm(request.POST, request.FILES)

#         if form.is_valid():
#             kyc_instance = form.save(commit=False)
#             kyc_instance.user = user
#             kyc_instance.save()

#             messages.success(request, "KYC information successfully submitted")
#             return redirect('account:account')
#         else:
#             print(form.errors)
#             messages.error(request, "Invalid form submission. Please check your inputs.")
#     else:
#         form = KycForm()
#     return render(request, 'account/kyc-form.html', {'form': form})


# # def kyc_registration_view(request):
#     user = request.user
#     print(user)
#     # account = get_object_or_404(Account, user=user)
#     # print(account)
#     try:
#         kyc = Kyc.objects.get(user=user)
#         form = KycForm(request.POST or None,
#                        request.FILES or None, instance=kyc)
#     except Kyc.DoesNotExist:
#         kyc = None
#         print('doesnt exist')
#         if request.method == "POST":
#             print('post')
#             form = KycForm(request.POST, request.FILES)
#             if not form.is_valid():
#                 print('invalid')
#             if form.is_valid():
#                 print('valid')
#                 new_form = form.save(commit=False)
#                 new_form.user = user
#                 # new_form.account = account
#                 # new_form.save()
#                 # print("suusuususuuuu")
#                 try:
#                     new_form.save()
#                 except Exception as e:
#                     print(f"Exception during form saving: {e}")

#                 messages.success(
#                     request, "Kyc successfully submitted, In review now")
#                 return redirect("account:account")
#         else:
#             form = KycForm()
#     context = {
#         'form': form,
#         'kyc': kyc,
#     }
#     return render(request, 'account/kyc-form.html', context)

# @login_required
# def kyc_registration_view(request):
#     user = request.user
#     account = get_object_or_404(Account, user=user)
#     try:
#         kyc = Kyc.objects.get(user=user)
#         form = KycForm(request.POST or None,
#                        request.FILES or None, instance=kyc)
#     except Kyc.DoesNotExist:
#         kyc = None
#         if request.method == "POST":
#             form = KycForm(request.POST, request.FILES)
#             if form.is_valid():
#                 new_form = form.save(commit=False)
#                 new_form.user = user
#                 new_form.account = account
#                 new_form.save()
#                 messages.success(
#                     request, "Kyc successfully submitted, In review now")
#                 return redirect("account:account")
#             else:
#                 for field, errors in form.errors.items():
#                     for error in errors:
#                         messages.error(
#                             request, f"{field.capitalize()}: {error}")

#         else:
#             form = KycForm(instance=kyc)
#     context = {
#         'account': account,
#         'form': form,
#         'kyc': kyc,
#     }
#     return render(request, 'account/kyc-form.html', context)
    
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

        except Kyc.DoesNotExist:
            messages.warning(request, "you need to submit kyc.")
            return redirect("account:kyc-form")
        sender_transaction = Transaction.objects.filter(
            sender=request.user).order_by("-id")
        receiver_transaction = Transaction.objects.filter(
            reciever=request.user).order_by("-id")
    else:
        messages.warning(request,  "You're not logged in.")
        return redirect("user_auth:sigin-in")
    context = {
        "kyc": kyc,
        "account": account,
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction
    }
    return render(request, "account/dashboard.html", context)
