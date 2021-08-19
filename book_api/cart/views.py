from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from book.models import Book
from cart.serializers import CartItemSerializer, CartSerializer, CartItemListSerializer

class CartView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.get(customer__id=self.user_id)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        return CartItemSerializer
    
    def get(self, request, *args, **kwargs):
        cart = self.get_queryset()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    # add to cart. If cartItem already exist, add order_quantity to its current order_quantity
    def post(self, request, *args, **kwargs):
        validated_data = get_validated_data(self.get_serializer, request)
        try:
            cart = Cart.objects.get(customer__id=self.user_id) # cart is created when customer register
            book = Book.objects.get(id=validated_data.get('book_id'))
            order_quantity = validated_data.get('order_quantity')
            with transaction.atomic():
                if order_quantity > book.quantity:
                    raise IntegrityError

                try: # cart item already exist
                    cartItem = CartItem.objects.get(book__id=book.id, cart__id=cart.id)                    
                    cartItem.order_quantity += order_quantity
                    if cartItem.order_quantity > book.quantity:
                        raise IntegrityError
                    cartItem.save()
                    return Response({'book_id': book.id, 'order_quantity': cartItem.order_quantity})
                except CartItem.DoesNotExist:
                    cartItem = CartItem.objects.create(
                                    book=book, 
                                    cart=cart,
                                    order_quantity=order_quantity
                                )
                    cartItem.save()
                    return Response(validated_data, status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'msg': f'There are only {book.quantity} items available'})
        except Book.DoesNotExist:
            return Response({'msg': 'Book id is not valid'}, status.HTTP_400_BAD_REQUEST)


    # create if cartItem not exist, replace order_quantity otherwise
    def put(self, request, format=None):
        validated_data = get_validated_data(self.get_serializer, request)
        try:
            cart = Cart.objects.get(customer__id=self.user_id)
            book = Book.objects.get(id=validated_data.get('book_id'))
            order_quantity = validated_data.get('order_quantity')
            with transaction.atomic():
                if order_quantity > book.quantity:
                    raise IntegrityError
                create_or_replace_cart_item(book, cart, order_quantity)
                return Response(validated_data, status.HTTP_200_OK)
        except IntegrityError:
            return Response({'msg': f'There are only {book.quantity} items available'})
        except Book.DoesNotExist:
            return Response({'msg': 'Book id is not valid'}, status.HTTP_400_BAD_REQUEST)        

    @property
    def user_id(self) -> int:
        return self.request.auth.payload.get('user_id')


class DeleteCartItem(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()


class MergeCart(APIView):
    permission_classes = (IsAuthenticated,)

    # request.data: {items: [{book_id, order_quantity}]}
    def post(self, request):
        validated_data = get_validated_data(CartItemListSerializer, request)
        customer_id = request.auth.payload.get('user_id')
        cart = Cart.objects.get(customer__id=customer_id)
        try:
            with transaction.atomic():
                for item in validated_data.get('items'):
                    book = Book.objects.get(id=item["book_id"])
                    order_quantity = item["order_quantity"]
                    if order_quantity > book.quantity:
                        raise IntegrityError
                    create_or_replace_cart_item(book, cart, order_quantity)
                return Response(validated_data, status.HTTP_200_OK)      
        except IntegrityError:
           return Response({'msg': f'There are some order quantity greater than availabe quantity.'}, 
                    status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'msg': 'Some book id is not valid'}, status.HTTP_400_BAD_REQUEST) 


def get_validated_data(serializer, request, raise_exception=True):
    s = serializer(data=request.data)
    s.is_valid(raise_exception=raise_exception)
    return s.validated_data

def create_or_replace_cart_item(book, cart, order_quantity):
    try:
        cartItem = CartItem.objects.get(book__id=book.id, cart__id=cart.id)                    
        cartItem.order_quantity = order_quantity
        cartItem.save()
    except CartItem.DoesNotExist:
        cartItem = CartItem.objects.create(
            book=book, cart=cart, 
            order_quantity=order_quantity)
        cartItem.save()