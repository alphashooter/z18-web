from django.contrib.auth.models import User
from django.forms import *
from .models import Currency


class LoginForm(Form):
    username = CharField(widget=TextInput({'class': 'form-control'}))
    password = CharField(widget=PasswordInput({'class': 'form-control'}))


class LoginForm2(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
