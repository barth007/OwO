from django.shortcuts import render, redirect
from django.views import View
from user_auth.kyc_forms import KYCForm
from django.contrib import messages


def submit_kyc(request):
    form = KYCForm(request.POST, request.FILES)
    if form.is_valid():
        kyc_instance = form.save(commit=False)
        kyc_instance.user = request.user  # Assuming the user is logged in
        kyc_instance.save()
        messages.success(request, 'KYC information submitted successfully.')
        return redirect('home')  # Redirect to a success page or wherever you want
    else:
        messages.error(request, 'Error submitting KYC information. Please check the form.')
        return render(request, 'kyc/kyc.html', {'form': form})
