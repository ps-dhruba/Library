from django.db import models
from django.contrib.auth.models import User
from Books.models import Borrowing

# Create your models here.
class DepositModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits = 12, decimal_places = 2)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('borrowing', 'Borrowing'),
        ('return', 'Return'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.SET_NULL, null=True, blank=True) # Link to Borrowing

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} - {self.timestamp}"