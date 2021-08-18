from customer.models import Customer
from book.models import Book
from django.db import models

# Create your models here.
class Cart(models.Model):
    total_amount = models.FloatField()
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through='CartItem')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id} - {self.customer.fullname}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.cart.id} -- {self.book.isbn} -- {self.order_quantity}'