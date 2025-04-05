from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='home'),
    path('games_review/', games_review, name='games'),
    path('order_review/', order_review, name='order'),
    path('game/<int:id>/', game_details, name="game_details"),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:game_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:game_id>/', cart_remove, name='cart_remove'),
    path('cart/update_quantity/<int:game_id>/', cart_update_quantity, name="cart_update_quantity")]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)