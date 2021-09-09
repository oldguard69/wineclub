from base.helpers import initialize_dotenv
import stripe
import os

initialize_dotenv()
stripe.api_key = os.getenv('stripe_sk')


requested_capabilities = ['card_payments', 'transfers'];
try:
    acc = stripe.Account.create(
        type='custom',
        business_type='company',
        company={
        "name":"pilot.businessName",
        "address":{
            "line1": "address 1",
            "city": "city 1",
            "country": "US",
            "state": "NY",
            "postal_code": "21201"
        }
        },
        country= "US",
        email= "test@email.com",
        # Assign a debit card to the Custom account as a payment method:
        # we use a test token for simplicity in this demo.
        external_account='tok_visa_debit',
        requested_capabilities=requested_capabilities,
    )
    print(acc)
except Exception as e:
    print(e)