from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
]