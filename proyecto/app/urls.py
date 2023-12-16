from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("cargar", cargar, name='cargar'),
    path("ingresar", ingresar, name='ingresar'),
    path("loadRS", loadRS, name='loadRS'),
]