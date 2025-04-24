from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Game, Order, Favorite
from .forms import OrderForm, GameForm, SignUpForm
from .cart import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'orders': orders,
        'favorites': favorites,
    })

def favorite_add(request, game_id):
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
        return JsonResponse({'is_favorite': is_favorite, 'game_id':game.id})
    return JsonResponse({'error':'Invalid request'}, status=400)

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    return render(request, 'home.html')

def games_review(request):
    games = Game.objects.all()
    favorites = Favorite.objects.filter(user=request.user).values_list('game_id', flat=True)
    return render(request, 'games_review.html', {'games': games, 'favorites':favorites})

def order_review(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect('cart_detail')
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = cart.get_total_price()
                order.count = sum(item["quantity"] for item in cart) #
                cart.clear()

                for item in cart:
                    game = item["game"]
                    quantity = item["quantity"]
                    if game.count < quantity:
                        return render(request, 'order_error.html')
                    game.count -= quantity
                    game.save()

                    cart.clear()
                    return render(request, "order_success.html", {'order':order})
    else:
        form = OrderForm(
            initial={
                "user": request.user,
                "total_price": cart.get_total_price(),
                "count": sum(item["quantity"] for item in cart),
            }
        )
    return render(request, 'order_review.html', {'form': form, 'cart':cart})    
#   if request.method == 'POST':
#       form = OrderForm(request.POST)
#       if form.is_valid():
#           order = form.save()
#           return redirect('order_success')
#   else:
#       form = OrderForm()
#   return render(request, 'order_review.html', {'form': form})

def game_details(request, id):
    try:
        game = Game.objects.get(id=id)
        return render(request, 'game_details.html', {'game': game})
    except Game.DoesNotExist:
        return render(request, 'game_details.html', {'game': None})
    
def cart_add(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(Game, id=game_id)
    cart.add(game=game)
    return render(request, 'order_success.html', {'success': cart})

def cart_remove(request, game_id):
    cart = Cart(request)
    game=get_object_or_404(Game, id=game_id)
    cart.remove(game=game)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

def cart_update_quantity(request, game_id):
    quantity = int(request.POST.get("quantity"))
    cart = Cart(request)
    game = get_object_or_404(Game, id = game_id)
    cart.update_quantity(game, quantity)
    new_total_price = cart.get_total_price()
    return redirect("cart_detail")
    #return JsonResponse({"new_total_price":new_total_price})
