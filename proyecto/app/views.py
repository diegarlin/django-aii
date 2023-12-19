from django.shortcuts import render, redirect, get_object_or_404

from .cargar import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import shelve
from .recommendations import  transformPrefs, getRecommendations, topMatches, getRecommendedItems, sim_distance

from .models import Anime
from django.db.models import Sum

def home(request):

    return render(request, 'index.html')

@login_required(login_url='/ingresar')
def cargar(request):
    
    cargar_datos()

    return render(request, 'index.html')

def ingresar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home')  
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'ingresar.html')



def loadDict():
    Prefs={}  
    shelf = shelve.open("dataRS")
    # ratings = Puntuacion.objects.all()
    ratings = []
    for ra in ratings:
        user = ra.id_usuario.id_usuario
        itemid = ra.id_pelicula.id_pelicula
        rating = ra.puntuacion
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf.close()

def loadRS(request):
    loadDict()
    messages.success(request, 'Se ha cargado la matriz')
    return redirect('home')

from django.shortcuts import render
from .models import Anime

def anime_por_genero(request):
    generos = Anime.objects.values_list('genre', flat=True).distinct()
    generos_separados = []

    for g in generos:
        splitted = g.split(',')
        for s in splitted:
            if s not in generos_separados:
                generos_separados.append(s)
    
    generos = generos_separados

    if request.method == 'POST':
        selected_genre = request.POST.get('genero')
        animes_por_formato = Anime.objects.filter(genre__contains=selected_genre).values('name', 'genre', 'type').annotate(total_episodes=Sum('episodes'))
        return render(request, 'anime_por_genero.html', {'generos': generos, 'animes_por_formato': animes_por_formato, 'selected_genre': selected_genre})

    return render(request, 'anime_por_genero.html', {'generos': generos})
