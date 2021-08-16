from django.db import models

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=200)
    data_of_birth = models.DateField(blank=True, null=True)
    info = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.fullname