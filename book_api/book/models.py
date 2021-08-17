from django.db import models
from django.db.models.base import Model

from genre.models import Genre
from publisher.models import Publisher
from author.models import Author


# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    quanity = models.IntegerField()
    price = models.FloatField()
    genre = models.ForeignKey(
                Genre, 
                on_delete=models.SET_NULL,
                null=True,
                blank=True
            )
    publisher = models.ForeignKey(
                    Publisher,
                    on_delete=models.SET_NULL,
                    null=True,
                    blank=True
                )
    author = models.ManyToManyField(Author)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.isbn} -- {self.title}'

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)