from base.helpers import initialize_dotenv
import stripe
import os

initialize_dotenv()
stripe.api_key = os.getenv('stripe_sk')

payment_method = stripe.PaymentMethod.create(
    type="card",
    card={
        "number": "4242424242424242",
        "exp_month": 9,
        "exp_year": 2022,
        "cvc": "314",
    }
)

print(payment_method)