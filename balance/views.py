from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DepositForm
from .models import DepositModel
from authenticate.models import RegisterModel
from decimal import Decimal
from Books.models import Borrowing
from django.core.mail import send_mail
from django.conf import settings

@login_required
def DepositView(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            try:
                register = RegisterModel.objects.get(user=request.user)
                register.deposit(amount)

                deposit = DepositModel.objects.create(user=request.user, amount=amount)

                #Email
                subject = "Deposit Successful"
                message = f"Dear {request.user.username},\n\nYour deposit of TK. {amount} has been successfully processed.\nYour new balance is TK. {register.balance}.\n\nThank you for using our service."
                from_email = settings.DEFAULT_FROM_EMAIL  # Use setting for from email
                recipient_list = [request.user.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                return redirect('home')

            except RegisterModel.DoesNotExist:
                print(f"No RegisterModel found for user: {request.user}")
                return redirect('home')

    else:
        form = DepositForm()

    try:
        register = RegisterModel.objects.get(user=request.user)
        balance = register.balance
    except RegisterModel.DoesNotExist:
        balance = 0

    return render(request, 'deposit.html', {'form': form, 'balance': balance})


@login_required
def transaction_view(request):
    user = request.user
    borrowed_books = Borrowing.objects.filter(user=user).order_by('-borrowed_date')

    borrowing_details = []
    current_balance = user.transaction_set.all().order_by('-timestamp').first().amount if user.transaction_set.exists() else Decimal('0.00')

    for borrowing in borrowed_books:
        borrowing_balance = current_balance
        borrowing_transactions = borrowing.transaction_set.all().order_by('timestamp')
        for transaction in borrowing_transactions:
            if transaction.transaction_type == 'borrowing':
                borrowing_balance -= transaction.amount
            elif transaction.transaction_type == 'return':
                borrowing_balance += transaction.amount
        borrowing_details.append({
            'borrowing': borrowing,
            'balance': borrowing_balance
        })
        current_balance = borrowing_balance

    try: 
        register = RegisterModel.objects.get(user=request.user)
        balance = register.balance 
    except RegisterModel.DoesNotExist:
        balance = 0

    return render(request, 'transaction.html', {
        'borrowing_details': borrowing_details,
        'current_balance': current_balance,
        'balance': balance, 
    })





