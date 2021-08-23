from django.db import models

from book.models import Book
from user.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_books = models.ManyToManyField(Book)
    # stripe_customer_id = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.fullname} - {self.email}'

