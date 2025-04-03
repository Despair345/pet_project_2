import json
from django.conf import settings
from .models import Game

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        print(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.session[settings.CART_SESSION_ID]
        self.cart = cart

    def add(self, game, quantity = 1, update_quantity = False):
        game_id = str(game.id)
        if game_id not in self.cart:
            self.cart[game_id] = {
                'quantity':0,
                'price':str(game.price),
                'title': game.title,
                'image': game.image.url,
            }
        if update_quantity:
            self.cart[game_id]['quantity'] = quantity
        else:
            self.cart[game_id]['quantity'] += quantity
        self.save()

    def remove(self, game):
        game_id = str(game.id)
        if game_id in self.cart:
            del self.cart[game_id]
            self.save()
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        game_ids = self.cart.keys()
        games = Game.objects.filter(id__in=game_ids)
        cart = self.cart.copy()
        for game in games:
            cart[str(game.id)]['game'] = game
        for item in cart.values():
            item['total_price'] = float(item['price']) * item['quantity']
            yield item

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified=True

    def get_total_price(self):
        return sum(float(item['price'])*item['quantity'] for item in self.cart.values())
        

    def update_quantity(self, game, quantity):
        game_id = str(game.id)
        if game_id in self.cart:
            self.cart[game_id]["quantity"]=quantity
            self.save()