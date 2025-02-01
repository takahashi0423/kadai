from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_search, name='product_search'),  
    path('search/', views.product_search, name='product_search'),  
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),  # 🛒 カートページ
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # 🛒 カートに追加
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # 🗑️ カートから削除
]
