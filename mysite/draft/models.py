from django.db import models

# Create your models here.

class Draft(models.Model):
    question = models.CharField(max_length=100)
    office = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    num = models.CharField(max_length=100)
    experience = models.CharField(max_length=300)
    experience2 = models.CharField(max_length=300)
    experience3 = models.CharField(max_length=300)
