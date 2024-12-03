from django.contrib import admin
from app.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'region', 'category', 'title', 'measurement', 'weight', 'quantity_per_pack', 'price')
    search_fields = ('code', 'title', 'category__title')
    list_filter = ('region', 'category')
