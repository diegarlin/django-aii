from django.shortcuts import render, redirect, get_object_or_404

from .cargar import *

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import shelve
from .recommendations import  transformPrefs, getRecommendations, topMatches, getRecommendedItems, sim_distance, calculateSimilarItems

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

