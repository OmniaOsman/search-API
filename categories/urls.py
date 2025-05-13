from .views import CategoryListView
from django.urls import path

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
]
