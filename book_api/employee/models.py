from user.models import User
from django.db import models

ROLE_CHOICES = [
    ('emp', 'Employee'),
    ('admin', 'Admin'),
]

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.FloatField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='emp')