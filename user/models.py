from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_retailer = models.BooleanField(default=False)

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


class ResetPasswordCode(models.Model):
    email = models.CharField(max_length=200)
    verify_code = models.UUIDField(unique=True)
    expiry_date = models.DateTimeField()