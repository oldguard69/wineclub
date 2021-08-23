from rest_framework import serializers

from order.models import Order, OrderDetail
from book.customer.serializers import BookSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ['customer']

    def get_items(self, obj):
        order_items = OrderDetail.objects.filter(order__id=obj.id)
        result = []
        for item in order_items:
            book = BookSerializer(data=item.book).data
            result.append({
                'book': book, 
                'order_quantity': item.order_qty,
                'price': item.price
            })
        return result