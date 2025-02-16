from django.shortcuts import render
from authenticate.models import RegisterModel
from Books.models import Books, Category


def homepage(request):
    balance = 0

    if request.user.is_authenticated:
        try:
            register = RegisterModel.objects.get(user=request.user)
            balance = register.balance
        except RegisterModel.DoesNotExist:
            RegisterModel.objects.create(user=request.user, balance=0)
            balance = 0

    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        try: 
            category_instance = Category.objects.get(name=selected_category)
            books = Books.objects.filter(categories=category_instance) 
        except Category.DoesNotExist:
            books = Books.objects.all() 
            selected_category = None

    else:
        books = Books.objects.all()

    return render(request, 'index.html', {
        'balance': balance,
        'books': books,
        'categories': categories,
        'selected_category': selected_category,
    })