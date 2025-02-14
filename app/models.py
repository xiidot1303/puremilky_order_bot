from django.db import models
from asgiref.sync import sync_to_async


REGIONS = [
    ('samarkand', "Samarkand"),
    ('tashkent', "Tashkent")
]


class Category(models.Model):
    uuid = models.CharField(null=True, max_length=64)
    title = models.CharField(null=True, max_length=255)
    region = models.CharField(null=True, choices=REGIONS, max_length=32)

    class Meta:
        unique_together = ('uuid', 'region')


class Product(models.Model):
    uuid = models.CharField(null=True, max_length=64)
    region = models.CharField(null=True, choices=REGIONS, max_length=32)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=255)
    measurement = models.CharField(null=True, max_length=8)
    weight = models.IntegerField(null=True)
    quantity_per_pack = models.IntegerField(null=True)
    price = models.BigIntegerField(null=True)
    remainder = models.BigIntegerField(null=True)
    photo = models.FileField(null=True, upload_to='product/photos/')

    class Meta:
        unique_together = ('uuid', 'region')


class Client(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True, unique=True)
    region = models.CharField(null=True, choices=REGIONS, max_length=32)
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

    class Meta:
        unique_together = ('uuid', 'region')

    def __str__(self) -> str:
        return self.name


class PriceType(models.Model):
    uuid = models.CharField(null=True, max_length=64)
    region = models.CharField(null=True, choices=REGIONS, max_length=32)
    product_uuid = models.CharField(null=True, max_length=64)
    price = models.IntegerField(null=True)

    class Meta:
        unique_together = ('uuid', 'region', 'product_uuid')


class OrderItem(models.Model):
    order = models.ForeignKey("app.Order", null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    count = models.IntegerField(null=True)
    price = models.BigIntegerField(null=True, default=0)


class Order(models.Model):
    bot_user = models.ForeignKey(
        'bot.Bot_user', null=True, blank=True, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, null=True, on_delete=models.PROTECT)
    datetime = models.DateTimeField(
        db_index=True, null=True, auto_now_add=True, blank=True)
    published = models.BooleanField(default=False, null=True)

    @property
    @sync_to_async
    def get_client(self):
        return self.client

    @property
    @sync_to_async
    def get_bot_user(self):
        return self.bot_user


class MinOrderAmount(models.Model):
    region = models.CharField(choices=REGIONS, max_length=32)
    amount = models.BigIntegerField()


class FavoritesItem(models.Model):
    favorites = models.ForeignKey(
        "app.Favorites", null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    count = models.IntegerField(null=True)


class Favorites(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)


class Feedback(models.Model):
    order = models.ForeignKey("app.Order", null=True,
                              blank=True, on_delete=models.CASCADE)
    comment = models.TextField(null=True, max_length=1024)
    datetime = models.DateTimeField(
        db_index=True, null=True, auto_now_add=True, blank=True)


class RecommendedOrder(models.Model):
    client = models.ForeignKey(
        'app.Client', null=True, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(
        'app.Product', null=True, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    region = models.CharField(null=True, choices=REGIONS, max_length=32)


class Bonus(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_free = models.BooleanField(default=True)
    condition_no_less = models.PositiveIntegerField(default=0)
    percentage_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    condition_no_less2 = models.PositiveIntegerField(default=0)
    percentage_amount2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    condition_no_less3 = models.PositiveIntegerField(default=0)
    percentage_amount3 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    condition_no_less4 = models.PositiveIntegerField(default=0)
    percentage_amount4 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    type_bonus = models.CharField(max_length=50)