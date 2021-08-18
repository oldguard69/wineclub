from django.db import models

# Create your models here.
class Role(models.Model):
    ROLE_CHOICES = [
        ('emp', 'Employee'),
        ('admin', 'Admin'),
    ]
    name = models.CharField(unique=True, max_length=10, default='emp')


class Employee(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=200)
    salary = models.FloatField()
    # role = models.ForeignKey(Role, on_delete=models.PROTECT)

    ROLE_CHOICES = [
        ('emp', 'Employee'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='emp')