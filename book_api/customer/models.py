from django.db import models


from book.models import Book
from user.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_books = models.ManyToManyField(Book)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.fullname} - {self.email}'

