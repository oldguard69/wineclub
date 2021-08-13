from django.db import models

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(unique=True, max_length=200)