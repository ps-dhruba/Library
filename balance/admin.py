from django.contrib import admin
from .models import DepositModel, Transaction

@admin.register(DepositModel)
class DepositModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')  # Customize display in admin
    search_fields = ('user__username',)  # Allow searching by username
    # Add any other fields you want to display/filter

@admin.register(Transaction)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'timestamp', 'borrowing')
    search_fields = ('user__username', 'transaction_type')
    list_filter = ('transaction_type',) # Add filters
    #raw_id_fields = ('borrowing',)  # If Borrowing FK is too slow, use thi
