from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    avatar = forms.CharField(max_length=300, help_text='Image URL')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','avatar',)
