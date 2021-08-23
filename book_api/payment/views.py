import os
import stripe
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv, find_dotenv

from book_api.helpers import get_user_id, get_validated_data
from customer.models import Customer
from payment.serializers import CreatePaymentIntentSerializer
from user.models import User

load_dotenv(find_dotenv())

# use this to collect card detail
class CreateSetupIntent(APIView):
    permission_classes = [IsAuthenticated]

    @property
    def user_id(self):
        return get_user_id(self.request)
    
    def get(self, request):
        customer = User.objects.get(user__id=self.user_id)
        setup_intent = stripe.SetupIntent.create(
            customer=customer.stripe_customer_id
        )
        return Response({'client_secrect': setup_intent.client_secrect})


class IsUserHasPaymentMethod(APIView):
    permission_classes = [IsAuthenticated]
    
    @property
    def user_id(self):
        return get_user_id(self.request)

    def get(self, request):
        customer = Customer.objects.get(self.user_id)
        payment_methods = stripe.PaymentMethod.list(
                customer=customer.stripe_customer_id,
                type='card'
        )

        if len(payment_methods):
            return Response({'msg': 'Have payment method'}, status.HTTP_200_OK)
        return Response({'msg': 'Does not have'}, status.HTTP_204_NO_CONTENT)


class GetPublishableKey(APIView):
    def get(self, request):
        return Response({'pk_key': os.getenv('stripe_pk')})

# body: {"currency", "amount"}
class CreatePaymentIntent(APIView):
    permission_classes = [IsAuthenticated]

    @property
    def user_id(self):
        return get_user_id(self.request)

    # use card in PaymentMethod to charge if it exist
    # otherwise, create PaymentIntent without card
    # webhook will attach card to customer.
    def post(self, request):
        validated_data, _ = get_validated_data(CreatePaymentIntentSerializer, request)
        order_amount = validated_data.get('amount')
        currency = validated_data.get('currency')
        
        try:
            customer = Customer.objects.get(self.user_id)
            stripe_customer_id = customer.stripe_customer_id
            # List the customer's payment methods to find one to charge
            payment_methods = stripe.PaymentMethod.list(
                customer=stripe_customer_id,
                type='card'
            )

            # use the exist card to charge
            if len(payment_methods['data']):
                # Create and confirm a PaymentIntent with the
                # order amount, currency, Customer and PaymentMethod IDs
                # If authentication is required or the card is declined, Stripe
                # will throw an error
                intent = stripe.PaymentIntent.create(
                    amount=order_amount,
                    currency=currency,
                    payment_method=payment_methods['data'][0]['id'],
                    customer=customer.stripe_customer_id,
                    confirm=True,
                    on_session=True
                )            
            else:
                # save card info during payment
                intent = stripe.PaymentIntent.create(
                    amount=order_amount,
                    currency=currency,
                    customer=stripe_customer_id,
                )

            return Response({
                    'publicKey': os.getenv('stripe_pk'),
                    'clientSecrect': intent.client_secrect
                })
        
        except stripe.error.CardError as e:
            err = e.error
            if err.code == 'authentication_required':
                # Bring the customer back on-session to authenticate the purchase
                # You can do this by sending an email or app notification to let them know
                # the off-session purchase failed
                # Use the PM ID and client_secret to authenticate the purchase
                # without asking your customers to re-enter their details
                return Response({
                    'error': 'authentication_required', 
                    'paymentMethod': err.payment_method.id, 
                    'amount': validated_data.get('amount'), 
                    'card': err.payment_method.card, 
                    'publicKey': os.getenv('stripe_pk'), 
                    'clientSecret': err.payment_intent.client_secret
                })
                
            elif err.code:
                # The card was declined for other reasons (e.g. insufficient funds)
                # Bring the customer back on-session to ask them for a new payment method
                return Response({
                    'error': err.code, 
                    'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY'), 
                    'clientSecret': err.payment_intent.client_secret
                })
