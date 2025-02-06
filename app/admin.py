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
    list_filter = ('days_of_the_week', 'region')


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
    list_display = ['id', 'bot_user', 'client', 'datetime', 'published']
    list_filter = ['datetime', 'bot_user', 'client']
    search_fields = ['client__name']  # Assuming Client has a `name` field
    ordering = ['-datetime']
    inlines = [OrderItemInline]  # Include OrderItems as inline


class FavoritesItemInline(admin.TabularInline):
    model = FavoritesItem
    extra = 1
    fields = ['product', 'count']
    readonly_fields = []


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ['id', 'client']
    list_filter = ['client']
    search_fields = ['client__name']
    inlines = [FavoritesItemInline]


@admin.register(MinOrderAmount)
class MinOrderAmountAdmin(admin.ModelAdmin):
    list_display = ['region', 'amount']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['order', 'comment']


@admin.register(RecommendedOrder)
class RecommendedOrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'product', 'quantity', 'region']
    list_filter = ['client', 'region']