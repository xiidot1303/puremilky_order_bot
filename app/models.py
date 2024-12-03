from django.db import models


class Category(models.Model):
    code = models.CharField(null=True, max_length=16)
    title = models.CharField(null=True, max_length=255)


REGIONS = [
    ('samarkand', "Samarkand"),
    ('tashkent', "Tashkent")
]


class Product(models.Model):
    code = models.CharField(null=True, max_length=16)
    region = models.CharField(null=True, choices=REGIONS, max_length=32)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=255)
    measurement = models.CharField(null=True, max_length=8)
    weight = models.IntegerField(null=True)
    quantity_per_pack = models.IntegerField(null=True)
    price = models.BigIntegerField(null=True)

