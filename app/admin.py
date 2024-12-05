from django.contrib import admin
from app.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title')
    search_fields = ('uuid', 'title')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'region', 'category', 'title',
                    'measurement', 'weight', 'quantity_per_pack', 'price')
    search_fields = ('uuid', 'title', 'category__title')
    list_filter = ('region', 'category')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'address', 'inn', 'branch_uuid', 'price_type_uuid',
        'phone', 'debt', 'latitude', 'longitude', 'date_last_visit', 'name_organization'
    )
    search_fields = ('name', 'inn', 'address', 'phone')
    list_filter = ('branch_uuid', 'price_type_uuid', 'days_of_the_week')
    list_editable = ('debt',)


@admin.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'product_uuid', 'price')
    search_fields = ('uuid', 'product_uuid')
    list_filter = ('price',)
