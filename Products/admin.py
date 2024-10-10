from django.contrib import admin
from .models import Products, Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'image_url']
    search_fields = ['name', 'category__name']
    list_filter = ['category']
admin.site.register(Products, ProductsAdmin)
