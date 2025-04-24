from django import forms
from .models import Order, Game
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta():
        model = User
        fields = ("username", "email", "password1", "password2")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "user",
            #"games", #is this correct?
            "count",
            "total_price",
            "country",
            "city",
            "address",
        ]
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "title",
            "description",
            "price",
            "image",
            "count",
        ]