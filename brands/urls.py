from .views import BrandListView
from django.urls import path


urlpatterns = [
    path('', BrandListView.as_view(), name='brand-list'),
]