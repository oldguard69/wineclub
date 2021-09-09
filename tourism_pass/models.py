from business.models import Business
from customer.models import Customer
from base.models import SoftDeletionModel
from django.db import models

class TourismPass(SoftDeletionModel):
    reward_points = models.IntegerField()
    qr_code = models.UUIDField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.FloatField()
    description = models.CharField(max_length=200, blank=True)
    is_bougth = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
