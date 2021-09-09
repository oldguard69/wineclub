from base.helpers import initialize_dotenv
import stripe
import os

initialize_dotenv()
stripe.api_key = os.getenv('stripe_sk')

product = stripe.Product.create(
    name="test",
    description="this is test product"
)

price = stripe.Price.create(
    unit_amount=2000,
    currency="gbp",
    recurring={"interval": "month"},
    product=product.id,
    lookup_key="test_product"
)

print(product.id)
print(price.id)