from django import forms
from .models import DepositModel

class DepositForm(forms.ModelForm):
    class Meta:
        model = DepositModel
        fields = ['amount']