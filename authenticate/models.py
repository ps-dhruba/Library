from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RegisterModel(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def deposit(self, amount):
        self.balance+=amount
        self.save()

    def __str__(self):
        return self.user.username