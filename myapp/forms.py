from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import *

User = get_user_model()

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'profile']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash password
        if commit:
            user.save()
        return user

def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

class UserSubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
        fields = ['plan']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'customer_name', 'email', 'address', 'payment_method', 'status']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }