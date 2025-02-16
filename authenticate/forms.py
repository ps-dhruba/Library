from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RegisterModel

class CreateUserForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11, required=True)
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)  # Don't save User yet
        if commit:
            user.save()  # Save User first
            RegisterModel.objects.create(  # Create RegisterModel instance
                user=user,
                address=self.cleaned_data.get('address', ''),  # Use get() to avoid KeyError
                phone_number=self.cleaned_data.get('phone_number', ''),
                balance=self.cleaned_data.get('balance', 0.00)
            )
        return user