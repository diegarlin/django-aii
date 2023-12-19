from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("cargar", cargar, name='cargar'),
    path("info", info, name='info'),
]