from django.db import models
from Categories.models import Category  # Assuming category model is defined in Categories app
from django.contrib.auth.models import User
from django.utils import timezone


class Books(models.Model):
    title = models.CharField(max_length=50)
    image_url = models.URLField(max_length=200, default='')  # Default empty string for image URL
    book_name = models.CharField(max_length=100, default='Unnamed Book')  # Default book name
    borrow_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Default price 0.0
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey to Category model
    quantity_available = models.PositiveIntegerField(default=0)  # Default quantity 0
    description = models.TextField(default='No description available')  # Default description

    def __str__(self):
        return self.title

class Comment(models.Model):
    book = models.ForeignKey(Books, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Assuming this is the commenter's name
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.name} on {self.book.book_name}"

class Order(models.Model):
    book = models.ForeignKey('Books', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} - {self.book.book_name} by {self.user.username}"
