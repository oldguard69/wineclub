from wine.models import Wine
from django.db import models
from base.models import BaseModel
from customer.models import Customer

class Cart(BaseModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)   
    wine = models.ManyToManyField(Wine, through='CartItem')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id} - {self.customer.fullname}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'cart_id: {self.cart.id} || {self.book.isbn} -- {self.order_quantity}'
