from business_category.models import BusinessCategory
from subscription.models import Subscription
from user.models import User
from base.models import SoftDeletionModel
from django.db import models

# flow for create a business
# 1. Create business, set stripe_customer_id
# 2. Paid subscription, set subscription and stripe_subscription_id
# 3. Create Connect Account, set stripe_account_id
class Business(SoftDeletionModel):
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True)
    stripe_subscription_id = models.CharField(max_length=200, blank=True)
    stripe_customer_id = models.CharField(max_length=200, blank=True)
    stripe_account_id = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['id']