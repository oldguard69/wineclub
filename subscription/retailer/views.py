import stripe
import os
from rest_framework.response import Response
from rest_framework.views import APIView
from subscription.models import Subscription
from rest_framework import status
stripe.api_key = os.getenv('stripe_sk')


from base.helpers import get_validated_data, get_user_id, response_message
from subscription.retailer.serializers import CancelStripeSubscriptionSerializer, CreateStripeSubscriptionSerializer
from business.models import Business

class SubscriptionPlans(APIView):
    def get(self, request):
        sub = Subscription.objects.all()
        lookup_key = [s.lookup_key for s in sub]
        prices = stripe.Price.list(
            lookup_keys=lookup_key
        )

        return Response(
            {
                "publishable_key": os.getenv('stripe_pk'),
                "prices": prices.data
            }
        )

class CreateSubscription(APIView):
    def post(self, request):
        validated_data, _ = get_validated_data(CreateStripeSubscriptionSerializer, request)
        try:
            price_id = validated_data.get('price_id')
            winery = Business.objects.get(user__id=get_user_id(request))
            
            subscription = stripe.Subscription.create(
                customer=winery.stripe_customer_id,
                items=[{
                    'price': price_id,
                }],
                default_payment_method="",
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent'],
            )
            
            return Response({
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret
            })
        except Exception as e:
            return Response(response_message(e.user_message))


class CancelSubscription(APIView):
    def post(self, request):
        validated_data, _ = get_validated_data(CancelStripeSubscriptionSerializer, request)
        try:
            # Cancel the subscription by deleting it
            deletedSubscription = stripe.Subscription.delete(validated_data.get('subscription_id'))
            return Response({"subscription": deletedSubscription})
        except Exception as e:
            return Response(response_message(str(e)), status.HTTP_400_BAD_REQUEST)