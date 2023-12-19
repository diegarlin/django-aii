from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("cargar", cargar, name='cargar'),
    path("ingresar", ingresar, name='ingresar'),
    path("loadRECSYS", loadRECSYS, name='loadRECSYS'),
    path("recomendar_animes", recomendar_animes, name='recomendar_animes'),
]