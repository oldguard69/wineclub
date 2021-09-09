from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import stripe

from base.helpers import response_message

class StripeWebhook(APIView):
    def post(self, request):
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        request_data = request.data

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']

        data_object = data['object']

        if event_type == 'invoice.payment_succeeded':
            if data_object['billing_reason'] == 'subscription_create':
                # The subscription automatically activates after successful payment
                # Set the payment method used to pay the first invoice
                # as the default payment method for that subscription
                subscription_id = data_object['subscription']
                payment_intent_id = data_object['payment_intent']

                # Retrieve the payment intent used to pay the subscription
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

                # Set the default payment method
                stripe.Subscription.modify(
                    subscription_id,
                    default_payment_method=payment_intent.payment_method
                )

                print("Default payment method set for subscription:" + payment_intent.payment_method)
        
         

        return Response(response_message('success'))