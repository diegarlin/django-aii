from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("cargar", cargar, name='cargar'),
    path("info", info, name='info'),
    path("loadRECSYS", loadRECSYS, name='loadRECSYS'),
    path("recomendar_animes", recomendar_animes, name='recomendar_animes'),
    path('animes_por_genero', anime_por_genero, name='animes_por_genero'),
    path('mejores_animes', mejores_animes, name='mejores_animes'),

]