from base.helpers import initialize_dotenv
import stripe
import os

initialize_dotenv()
stripe.api_key = os.getenv('stripe_sk')

pm = stripe.PaymentMethod.list(customer='cus_KAyKorzyxD2XKb', type='card')
print(pm)