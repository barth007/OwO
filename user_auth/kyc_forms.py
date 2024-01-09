from django import forms
from user_auth.kyc_models import KYC

class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = [
            'next_of_kin',
            'bvn',
            'phone_number',
            'nok_phone_number',
            'residential_address',
            'sex',
            'means_of_identification',
            'picture_upload',
        ]

    def __init__(self, *args, **kwargs):
        super(KYCForm, self).__init__(*args, **kwargs)
        self.fields['next_of_kin'].widget.attrs['placeholder'] = 'Enter Next of Kin'
        self.fields['bvn'].widget.attrs['placeholder'] = 'Enter BVN'
        self.fields['residential_address'].widget.attrs['placeholder'] = 'Enter Residential Address'
        self.fields['sex'].widget.attrs['placeholder'] = 'Select Sex'
        self.fields['means_of_identification'].widget.attrs['placeholder'] = 'Select Means of Identification'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Valid Phone number'
        self.fields['nok_phone_number'].widget.attrs['placeholder'] = 'Enter Valid Phone Number'


