from django.db import models
from base.models import SoftDeletionModel

class Subscription(SoftDeletionModel):
    name = models.CharField(max_length=200)
    lookup_key = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    stripe_product_id = models.CharField(max_length=200, blank=True)
    stripe_price_id = models.CharField(max_length=200, blank=True)