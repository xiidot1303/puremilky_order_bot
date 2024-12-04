from django.contrib import admin
from app.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title')
    search_fields = ('uuid', 'title')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'region', 'category', 'title', 'measurement', 'weight', 'quantity_per_pack', 'price')
    search_fields = ('uuid', 'title', 'category__title')
    list_filter = ('region', 'category')
