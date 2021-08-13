from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(unique=True)


class Admin(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    password = models.CharField()
    salary = models.FloatField()
    role = models.ForeignKey(Role)