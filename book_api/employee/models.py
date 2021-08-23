from django.db import models

from soft_deletion.models import SoftDeletionModel
from user.models import User

ROLE_CHOICES = [
    ('emp', 'Employee'),
    ('admin', 'Admin'),
]

class Employee(SoftDeletionModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.FloatField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='emp')

    class Meta:
        ordering = ['id']