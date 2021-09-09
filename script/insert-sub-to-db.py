from subscription.models import Subscription

s = Subscription.objects.create(
    name="test",
    stripe_product_id="prod_KBL7mqi6ScHmbJ",
    stripe_price_id="price_1JWyR6LrHj4rBroeTZAgQcmo",
    lookup_key="test_produc1t"
)
s.save()