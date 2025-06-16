from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('modal/', views.modal, name='modal'),
    path('klavesin/', views.klavesin, name='klavesin'),
    path('organ/', views.organ, name='organ')
]

