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
        # Explicitly set the 'user' field when creating a new Kyc instance
        form = KycForm(request.POST or None, request.FILES or None, initial={'user': user})

    if request.method == "POST":
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(
                request, "Kyc successfully submitted, In review now")
            return redirect("account:account")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    context = {'account': account, 'form': form, 'kyc': kyc}
    return render(request, 'account/kyc-form.html', context)