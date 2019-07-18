from django.urls import path

from . import views

urlpatterns = [
    path('price-comparison', views.PriceComparison.as_view(), name='compare'),
]
