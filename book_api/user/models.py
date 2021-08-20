from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


# User is base Model.
# Employee has salary, role
# Customer has cart, favorite book
class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

    class Meta:
        ordering = ['id']
    

class UpdateEmailVerifyCode(models.Model):
    current_email = models.EmailField()
    new_email = models.EmailField()
    verify_code = models.UUIDField()
    expiry_date = models.DateTimeField()