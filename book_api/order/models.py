from django.db import models

from customer.models import Customer
from book.models import Book

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('cancel', 'Cancel'),
        ('success', 'Success')
    ]
    status = models.CharField(choices=ORDER_STATUS, default='pending')
    total_price = models.FloatField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    customer = models.ForeignKey(Customer)
    books = models.ManyToManyField(Book, through='OrderDetail')

class OrderDetail(models.Model):
    order = models.ForeignKey(Order)
    book = models.ForeignKey(Book)
    order_qty = models.SmallIntegerField()
    price = models.FloatField()