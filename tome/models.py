from django.db import models
from jutsu.models import Jutsu
from django.contrib.auth.models import User


class Tome(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jutsus = models.ManyToManyField(to=Jutsu, related_name='tome', blank=True)

    def id(self):
        return self.id

    def __str__(self):
        return str(self.name) + ' (' + self.user.username + ')'
