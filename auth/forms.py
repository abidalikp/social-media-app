from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):

    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=254)
    last_name = forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'username', 'password1', 'password2')