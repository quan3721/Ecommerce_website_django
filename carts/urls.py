from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'), # url cart page
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'), # url for adding item into cart
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'), # url for decreasing item into cart
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
]
