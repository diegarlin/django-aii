from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Anime(models.Model):
    anime_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    episodes = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Puntuacion(models.Model):
    user_id = models.IntegerField(default=0)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.user.username} - {self.anime.name} - {self.rating}"
