from django.db import models


class Category(models.Model):
    uuid = models.CharField(null=True, max_length=64, unique=True)
    title = models.CharField(null=True, max_length=255)


REGIONS = [
    ('samarkand', "Samarkand"),
    ('tashkent', "Tashkent")
]


class Product(models.Model):
    uuid = models.CharField(null=True, max_length=64, unique=True)
    region = models.CharField(null=True, choices=REGIONS, max_length=32)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=255)
    measurement = models.CharField(null=True, max_length=8)
    weight = models.IntegerField(null=True)
    quantity_per_pack = models.IntegerField(null=True)
    price = models.BigIntegerField(null=True)
    photo = models.FileField(null=True, upload_to='product/photos/')


class Client(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    inn = models.CharField(max_length=64, blank=True, null=True)
    branch_uuid = models.CharField(max_length=36, blank=True, null=True)
    price_type_uuid = models.CharField(max_length=36, blank=True, null=True)
    days_of_the_week = models.JSONField(blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    debt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    latitude = models.CharField(max_length=64, blank=True, null=True)
    longitude = models.CharField(max_length=64, blank=True, null=True)
    date_last_visit = models.DateTimeField(blank=True, null=True)
    name_organization = models.CharField(max_length=255, blank=True, null=True)


class PriceType(models.Model):
    uuid = models.CharField(null=True, max_length=64)
    product_uuid = models.CharField(null=True, max_length=64)
    price = models.IntegerField(null=True)


class OrderItem(models.Model):
    order = models.ForeignKey("app.Order", null=True, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    count = models.IntegerField(null=True)


class Order(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.PROTECT)
    datetime = models.DateTimeField(
        db_index=True, null=True, auto_now_add=True, blank=True)
