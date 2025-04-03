from django import forms
from .models import Order, Game

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "user",
            "games",
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