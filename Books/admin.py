from django.contrib import admin
from .models import Category, Books, Borrowing, Review  # Import all your models

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'borrowing_price', 'get_categories')  # Display categories
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)  # For ManyToMany fields

    def get_categories(self, obj):  # Display categories as a string
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'  # Set column header


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'returned_date', 'borrowing_price')
    search_fields = ('user__username', 'book__title')
    list_filter = ('returned_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    search_fields = ('book__title', 'user__username')
    list_filter = ('rating',)
    raw_id_fields = ('book', 'user') # For large datasets, use raw_id_fields