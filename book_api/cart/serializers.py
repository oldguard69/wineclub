from rest_framework import serializers


from cart.models import Cart, CartItem
from book.models import Book
from book.customer.serializers import BookSerializer


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('items', )

    def get_items(self, obj):
        CartItems = CartItem.objects.filter(cart__id=obj.id)
        result = []
        for item in CartItems:
            book = BookSerializer(item.book).data
            result.append({'book': book, 'order_quantity': item.order_quantity, 'id': item.id})
        return result

class CartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    order_quantity = serializers.IntegerField()

class CartItemListSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)