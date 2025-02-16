from django.contrib import admin
from django.urls import path
from authenticate.views import registerPage, login_view, logout_view
from django.conf.urls.static import static
from django.conf import settings
from balance.views import DepositView, transaction_view
from Books.views import borrow_book, return_book, book_details, profilePage, review_book
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name = 'home'),
    path('deposit/', DepositView, name = 'deposit'),
    path('profile/', profilePage, name = 'profile'),
    path('register/', registerPage, name = 'register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('transaction/', transaction_view, name = 'transaction'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow'),
    path('return/<int:borrowing_id>/', return_book, name='return'),
    path('details/<str:book_name>/', book_details, name='book_details'),
    path('return/<int:borrowing_id>/', return_book, name='return'),
    path('books/<int:book_id>/review/', review_book, name='review_book'),
]

if settings.DEBUG:  # Very important! Only in development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
