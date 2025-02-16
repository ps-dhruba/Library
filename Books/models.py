from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Books(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book_category', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='book_categories')
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    borrowing_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
    
class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    borrowing_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} on {self.borrowed_date}"

class Review(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) 
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"
