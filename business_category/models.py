from base.models import SoftDeletionModel
from django.db import models

class BusinessCategory(SoftDeletionModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['id']
