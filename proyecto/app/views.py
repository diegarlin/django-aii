from django.shortcuts import render, redirect

from .cargar import *
from django.contrib import messages
from .cargar import cargar_datos
from .models import Anime, Puntuacion
import shelve
from .recommendations import  transformPrefs, getRecommendations, calculateSimilarItems

from .models import Anime
from django.db.models import Sum

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


def cargarRECSYS():
    Prefs={}  
    shelf = shelve.open("dataRECSYS")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = ra.user_id
        itemid = ra.anime.anime_id
        rating = ra.rating
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf.close()

def loadRECSYS(request):
    cargarRECSYS()
    messages.success(request, 'Se ha cargado la matriz')
    return redirect('home')

def recomendar_animes(request):
    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        formato_emision = request.POST.get('formato_emision')

        shelf = shelve.open("dataRECSYS")
        Prefs = shelf['Prefs']
        shelf.close()
        rankings = getRecommendations(Prefs, user_id)
        
        
        animes = []       
        puntuaciones = []

        for re in rankings:
            anime = Anime.objects.get(pk=re[1])
            if anime.type == formato_emision:
                animes.append(Anime.objects.get(pk=re[1]))
                puntuaciones.append(re[0])


        items = zip(animes[:2], puntuaciones[:2])
        tipos_de_emision = Anime.objects.values_list('type', flat=True).distinct()
        return render(request, 'recomendaciones.html', {'items': items, 'user_id': user_id, 'tipos_de_emision': tipos_de_emision})

    tipos_de_emision = Anime.objects.values_list('type', flat=True).distinct()
    return render(request, 'recomendaciones.html', {'tipos_de_emision': tipos_de_emision})

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
