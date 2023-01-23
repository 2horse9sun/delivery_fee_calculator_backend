from django.urls import path

from . import views

urlpatterns = [
    path('calculate/', views.calculate_delivery_fee, name='calculate_delivery_fee'),
]