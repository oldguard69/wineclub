from base.helpers import initialize_dotenv
import stripe
import os

initialize_dotenv()
stripe.api_key = os.getenv('stripe_sk')

# product = stripe.Product.create(
#     name="test",
#     description="this is test product"
# )

try:
    price = stripe.Price.modify(
        'price_1JWyR6LrHj4rBroeTZAgQcmo',
        lookup_key="test_produc1t"
    )
except Exception as e:
    print(e)

# print(product.id)
print(price.id)
