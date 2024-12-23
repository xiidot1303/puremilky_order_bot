from django.contrib import admin
from app.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'region')
    search_fields = ('uuid', 'title')
    list_filter = ('region', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'region', 'category', 'title',
                    'measurement', 'weight', 'quantity_per_pack', 'price', 'photo')
    search_fields = ('uuid', 'title', 'category__title')
    list_filter = ('region', 'category')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'name_organization', 'region'
    )
    search_fields = ('name', 'address', 'phone', 'region')
    list_filter = ( 'days_of_the_week', 'region')


@admin.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'product_uuid', 'price', 'region')
    search_fields = ('uuid', 'product_uuid')
    list_filter = ('price', 'region')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of extra empty forms for related OrderItem
    fields = ['product', 'count', 'price']
    readonly_fields = []


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'datetime', 'published']
    list_filter = ['datetime', 'client']
    search_fields = ['client__name']  # Assuming Client has a `name` field
    ordering = ['-datetime']
    inlines = [OrderItemInline]  # Include OrderItems as inline
