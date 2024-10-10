from django.db import models
from Products.models import Products
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    rating = models.PositiveIntegerField()  # Rating 
    comment = models.TextField(null=True, blank=True)  # Optional comment
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically add review date

    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.rating}/5)'

    class Meta:
        unique_together = ['user', 'product']  # One review per user per product
