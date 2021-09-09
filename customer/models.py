from business.models import Business
from django.db import models

from base.models import SoftDeletionModel
from user.models import User
from reward_program.models import RewardProgram
from wine.models import Wine


class Customer(SoftDeletionModel):
    reward_points = models.IntegerField(default=0)
    stripe_customer_id = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_region = models.CharField(max_length=300, blank=True)
    favorite_wine_type = models.CharField(max_length=200, blank=True)

    reward_program = models.ManyToManyField(RewardProgram, through='CustomerRewardProgram')
    favorite_wine = models.ManyToManyField(Wine)
    favorite_business = models.ManyToManyField(Business)

class CustomerRewardProgram(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reward_program = models.ForeignKey(RewardProgram, on_delete=models.CASCADE)
    is_used = models.BooleanField()