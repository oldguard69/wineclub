from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from book.models import Book
from cart.serializers import CartItemSerializer, CartSerializer, CartItemListSerializer

# TODO: update book quantity field
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
        print(cart)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    # add to cart. If cartItem already exist, add order_quantity to its current order_quantity
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            cart = Cart.objects.get(customer__id=self.user_id) # cart is created when customer register
            book = Book.objects.get(id=validated_data.get('book_id'))
            order_quantity = validated_data.get('order_quantity')
            with transaction.atomic():
                if order_quantity > book.quanity:
                    raise IntegrityError

                try: # cart item already exist
                    cartItem = CartItem.objects.get(book__id=book.id, cart__id=cart.id)                    
                    cartItem.order_quantity += order_quantity
                    if cartItem.order_quantity > book.quanity:
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
                    return Response(serializer.data, status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'msg': f'There are only {book.quanity} items available'})
        except Book.DoesNotExist:
            return Response({'msg': 'Book id is not valid'}, status.HTTP_400_BAD_REQUEST)


    # create if cartItem not exist, replace order_quantity otherwise
    def put(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            cart = Cart.objects.get(customer__id=self.user_id) # cart is created when customer register
            book = Book.objects.get(id=validated_data.get('book_id'))
            order_quantity = validated_data.get('order_quantity')
            with transaction.atomic():
                if order_quantity > book.quanity:
                    raise IntegrityError
                try: # cart item already exist
                    cartItem = CartItem.objects.get(book__id=book.id, cart__id=cart.id)                    
                    cartItem.order_quantity = order_quantity
                    cartItem.save()
                except CartItem.DoesNotExist:
                    cartItem = CartItem.objects.create(book=book, cart=cart, order_quantity=order_quantity)
                    cartItem.save()
                return Response(serializer.data, status.HTTP_200_OK)
        except IntegrityError:
            return Response({'msg': f'There are only {book.quanity} items available'})
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

    def post(self, request):
        serializer = CartItemListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_id = request.auth.payload.get('user_id')
        cart = Cart.objects.get(customer__id=customer_id)
        try:
            with transaction.atomic():
                for item in serializer.validated_data.get('items'):
                    book = Book.objects.get(id=item["book_id"])
                    order_quantity = item["order_quantity"]
                    if order_quantity > book.quanity:
                        raise IntegrityError
                    
                    try: # cart item already exist
                        cartItem = CartItem.objects.get(book__id=book.id, cart__id=cart.id)                    
                        cartItem.order_quantity = order_quantity
                        cartItem.save()
                    except CartItem.DoesNotExist:
                        cartItem = CartItem.objects.create(
                            book=book, cart=cart, 
                            order_quantity=order_quantity)
                        cartItem.save()
                return Response(serializer.data, status.HTTP_200_OK)      
        except IntegrityError:
           return Response({'msg': f'There are some order quantity greater than availabe quantity.'}, 
                    status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'msg': 'Some book id is not valid'}, status.HTTP_400_BAD_REQUEST) 
