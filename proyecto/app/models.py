from django.db import models
from django.contrib.auth.models import User

class Anime(models.Model):
    anime_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    episodes = models.IntegerField()

    def __str__(self):
        return self.name

class Puntuacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.anime.name} - {self.rating}"

