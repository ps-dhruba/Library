from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Books, Borrowing, Review
from authenticate.models import RegisterModel
from balance.models import Transaction
from .forms import ReviewForm
from django.http import Http404 
from django.utils import timezone
from django.http import HttpResponse
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Books, pk=book_id)

    try:
        register = RegisterModel.objects.get(user=request.user)
        if register.balance >= book.borrowing_price:
            borrowing = Borrowing.objects.create(
                user=request.user, 
                book=book, 
                borrowing_price=book.borrowing_price
            )

            register.balance -= book.borrowing_price
            register.save()

            Transaction.objects.create(
                user=request.user,
                amount=book.borrowing_price,
                transaction_type='borrowing', 
                borrowing=borrowing 
            )

            # Email)
            subject = f"You have borrowed '{book.title}'"
            message = f"Dear {request.user.username},\n\nYou have successfully borrowed '{book.title}'.\nBorrowing details:\nBorrowing ID: {borrowing.id}\nBook: {book.title}\nPrice: {book.borrowing_price}\n\nThank you for using our library services."

            send_mail(
                subject,
                message,  
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
            )

            return redirect('profile')  
        else:
            # Insufficient balance
            return HttpResponse("Not enough funds. Please try again later.")

    except RegisterModel.DoesNotExist:
        raise Http404("User profile not found.") 
    except Exception as e: 
        print(f"An error occurred: {e}") 
        return HttpResponse("An error occurred. Please try again later.")

@login_required
def return_book(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id, user=request.user)

    if borrowing.returned_date is not None:
        return HttpResponse("This book has already been returned.")

    if request.method == 'POST': 
        borrowing.returned_date = timezone.now()
        borrowing.save()

        try:
            register = RegisterModel.objects.get(user=request.user)
            register.balance += borrowing.borrowing_price  
            register.save()

            Transaction.objects.create(
                user=request.user,
                amount=borrowing.borrowing_price,
                transaction_type='return',  
                borrowing=borrowing 
            )

            return redirect('home')

        except RegisterModel.DoesNotExist:
            raise Http404("User profile not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return HttpResponse("An error occurred. Please try again later.") 

    return HttpResponse("Invalid request method") 

@login_required
def profilePage(request):
    try:
        register = RegisterModel.objects.get(user=request.user)
        borrowed_books = Borrowing.objects.filter(user=request.user).order_by('-borrowed_date')

        borrowing_details = []
        current_balance = request.user.transaction_set.all().order_by('-timestamp').first().amount if request.user.transaction_set.exists() else Decimal('0.00')

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

        return render(request, 'profile.html', {
            'register': register,
            'borrowing_details': borrowing_details,
            'balance': register.balance 
        })

    except RegisterModel.DoesNotExist:
        return redirect('register')


@login_required
def review_book(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_details', book_name=book.title) 
    else:
        form = ReviewForm()
    return render(request, 'details.html', {'form': form, 'book': book})

def book_details(request, book_name):
    book = get_object_or_404(Books, title=book_name)
    form = ReviewForm()

    if request.user.is_authenticated:
        has_borrowed_book = Borrowing.objects.filter(user=request.user, book=book).exists()
    else:
        has_borrowed_book = False

    return render(request, 'details.html', {'book': book, 'form': form, 'has_borrowed_book': has_borrowed_book})
