from django.db import models


from book.models import Book

# Create your models here.
class Customer(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(blank=True, max_length=15)
    address = models.TextField(blank=True)
    password = models.CharField(max_length=200)
    date_join = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    favorite_books = models.ManyToManyField(Book)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.fullname} - {self.email}'

class UpdateEmailVerifyCode(models.Model):
    current_email = models.EmailField()
    new_email = models.EmailField()
    verify_code = models.UUIDField()
    expiry_date = models.DateTimeField()