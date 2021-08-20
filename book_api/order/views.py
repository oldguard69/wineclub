from rest_framework import status
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from cart.models import CartItem, Cart
from book.models import Book
from order.models import Order, OrderDetail
from customer.models import Customer
# Create your views here.
class CreateOrder(APIView):
    permission_classes = (IsAuthenticated,)

    @property
    def customer_id(self):
        return self.request.auth.payload.get('user_id')

    def get(self, request):
        cart = Cart.objects.get(customer__id=self.customer_id)
        cart_items = CartItem.objects.filter(cart__id=cart.id)
        if len(cart_items) == 0:
            return Response({'msg': 'There are no book in your cart.'})
        
        total_price = 0
        customer = Customer.objects.get(id=self.customer_id)
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    customer=customer,
                    total_price=total_price
                )
                order.save()
                for item in cart_items:
                    book = Book.objects.get(id=item.book.id)
                    if item.order_quantity > book.quantity:
                        raise IntegrityError
                    order_quantity = item.order_quantity
                    price = book.price
                    total_price += order_quantity * price
                    order_item = OrderDetail(
                        order=order, book=book, 
                        order_qty=order_quantity, price=price
                    )
                    order_item.save()
                    item.delete()
                    book.quantity -= order_quantity
                    book.save()
                order.total_price = total_price
                order.save()
        except IntegrityError:
            return Response(
                {'msg': 'There are one order item with quantity greater than available quantity'},
                status.HTTP_400_BAD_REQUEST
            )  
        

"""
1. create order
2. for each item in cart
    2.1. check quantity
    2.2. create order_item
    2.3. delete cart_item
    2.4. update book_quantity
"""