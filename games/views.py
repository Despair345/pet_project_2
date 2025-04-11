from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Game, Order
from .forms import OrderForm, GameForm, SignUpForm
from .cart import Cart
from django.http import JsonResponse

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
    return render(request, 'games_review.html', {'games': games})

def order_review(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'order_review.html', {'form': form})

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