from django.db import models


class Animales(models.Model):
    id = models.AutoField(primary_key=True)
    especie = models.CharField(max_length=10)
    nombre = models.CharField(max_length=15)
    numero = models.IntegerField(default=1,)
    comida = models.IntegerField()
    user_id = models.IntegerField()
