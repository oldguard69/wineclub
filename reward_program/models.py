from business.models import Business
from django.db import models

# if Program still has valid time and one of the conditions
# 1) Total purchase amount gte total_amount
# 2) Customer's ordered wines gte total_wine_purchased
# they will get reward point
class RewardProgram(models.Model):
    reward_code = models.UUIDField()
    reward_points = models.IntegerField()
    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    total_amount = models.FloatField()
    total_wine_purchased = models.IntegerField()
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

