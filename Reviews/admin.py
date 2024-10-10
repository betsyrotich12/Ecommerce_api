from django.contrib import admin
from .models import Review

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username']
    list_filter = ['rating', 'product']
admin.site.register(Review, ReviewAdmin)