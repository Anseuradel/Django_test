from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import TemplateView

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Algo(models.Model):
    name=models.CharField(max_length=100)
    vehicules=models.IntegerField()
    vehicule_dispo=models.IntegerField()
    nbre_transport=models.IntegerField()
    nbre_demande_exclusif = models.IntegerField()
    ratio = models.FloatField()

