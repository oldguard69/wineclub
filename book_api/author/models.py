from django.db import models

from soft_deletion.models import SoftDeletionModel

class Author(SoftDeletionModel):
    fullname = models.CharField(max_length=200)
    data_of_birth = models.DateField(blank=True, null=True)
    info = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.fullname