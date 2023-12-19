from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from .cargar import cargar_datos
from .models import Anime, Puntuacion

def home(request):
    return render(request, 'index.html')

def cargar(request):
    if request.method == 'POST':
        if 'confirmar' in request.POST:
            cargar_datos()
            return redirect('info')

    return render(request, 'confirmacion.html')

def info(request):
    num_animes = Anime.objects.count()
    num_puntuaciones = Puntuacion.objects.count()

    return render(request, 'info.html', {'num_animes': num_animes, 'num_puntuaciones': num_puntuaciones})
