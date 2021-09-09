from base.models import SoftDeletionModel
from django.db import models
from business.models import Business

class Wine(SoftDeletionModel):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.CharField(max_length=200, blank=True)
    reward_points = models.IntegerField(default=0)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']