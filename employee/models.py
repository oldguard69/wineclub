from user.models import User
from base.models import SoftDeletionModel
from django.db import models


from base.constants import ROLE_CHOICES, EMP_ROLE

class Employee(SoftDeletionModel):
    salary = models.FloatField(default=0.0)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=EMP_ROLE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
