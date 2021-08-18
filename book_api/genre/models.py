from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(unique=True, max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.name