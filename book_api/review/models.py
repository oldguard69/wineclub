from django.db import models

from book.models import Book
from customer.models import Customer

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()    
    rating = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
