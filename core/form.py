from django import forms
from core.models import CreditCard


class CreditCardForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={"placeHolder": "Card Holder Name"}))
    number = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeHolder": "Card Number"}))
    month = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeHolder": "Expiry month"}))
    year = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeHolder": "Expiry Year"}))
    cvv = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeHolder": "CVV Number"}))

    class Meta:
        model = CreditCard
        fields = ["name", "number", "month", "year", "cvv", "card_type"]
