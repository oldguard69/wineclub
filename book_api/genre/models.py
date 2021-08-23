from django.db import models

from soft_deletion.models import SoftDeletionModel

class Genre(SoftDeletionModel):
    name = models.CharField(unique=True, max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.name