from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Anime, Puntuacion

def cargar_datos():
    borrar_datos()
    cargar_animes()
    cargar_puntuaciones()

def borrar_datos():
    Puntuacion.objects.all().delete()
    Anime.objects.all().delete()

def cargar_animes():
    with open('datasets/anime.txt', 'r') as file:
        next(file)  # Omitir la cabecera
        animes_lines = file.readlines()
        for line in animes_lines:
            anime_data = line.strip().split('\t')
            anime_id, name, genre, anime_type, episodes = anime_data

            # Manejar el caso de 'Unknown' en el campo 'episodes'
            episodes = episodes if episodes.lower() != 'unknown' else None

            Anime.objects.create(
                anime_id=anime_id,
                name=name,
                genre=genre,
                type=anime_type,
                episodes=episodes
            )

def cargar_puntuaciones():
    with open('datasets/ratings.txt', 'r') as file:
        next(file)
        puntuaciones_lines = file.readlines()
        for line in puntuaciones_lines:
            puntuacion_data = line.strip().split('\t')
            user_id, anime_id, rating = puntuacion_data
            try:
                anime = Anime.objects.get(anime_id=anime_id)
                Puntuacion.objects.create(
                    user_id=user_id,
                    anime=anime,
                    rating=rating
                )
            except ObjectDoesNotExist:
                print(f"Error: No se puede encontrar Anime con ID {anime_id}")
