from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Game, Order, Favorite
from .forms import *
from .cart import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db import transaction

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'orders': orders,
        'favorites': favorites,
    })

def is_admin(user):
    return user.groups.filter(name='Admin').exists()
from django.db.models import Sum, Count
from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncDate
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum("total_price"))['total'] or 0
    top_games = (
        Order.objects.values('games__title').annotate(total_sold=Sum('count').order_by('-total_sold'))[:5]
    )
    today = now().date()    
    last_week = today - timedelta(days=6)
    orders_per_day = (
        Order.objects.filter(created_at__date__range=[last_week, today])
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    return render(request, 'admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'top_games': top_games,
        'orders_per_day': orders_per_day,
    })


@login_required
@user_passes_test(is_admin)
def add_new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('game_add')
    else:
        form = GameForm()
    return render(request, 'add_game.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def assign_user_to_group(request):
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = UserGroupForm()
    return render(request, 'assign_group.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def remove_game(request):
    if request.method == 'POST':
        form = GameDeleteForm(request.POST)
        if form.is_valid():
            form.delete()
            return redirect('admin')
    else:
        form = GameDeleteForm()
    return render(request, 'remove_game.html', {'form': form})

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
            group = Group.objects.get(name="User")
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    is_admin = request.user.groups.filter(name='Admin').exists()
    return render(request, 'home.html', {'is_admin':is_admin})

def games_review(request):
    games = Game.objects.all()
