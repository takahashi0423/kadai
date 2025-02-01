from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_search, name='product_search'),  # 空のパスにビューを割り当て
    path('search/', views.product_search, name='product_search'),  # search/でも利用可能
]
