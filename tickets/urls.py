from django.urls import path

from . import views

urlpatterns = [
    path('', views.PriceComparison.as_view(), name='compare'),
]
