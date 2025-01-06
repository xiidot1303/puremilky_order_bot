from rest_framework import serializers
from adrf.serializers import Serializer, ModelSerializer
from app.models import *
from bot.models import Bot_user
from asgiref.sync import sync_to_async


class ProductSerializer(ModelSerializer):
    price_for_client = serializers.CharField()

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OrderItemSerializerByData(ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'count', 'price']


class OrderSerializerByData(ModelSerializer):
    client = serializers.SlugRelatedField(
        queryset=Client.objects.all(),
        slug_field='id'
    )
    order_items = OrderItemSerializerByData(many=True)

    class Meta:
        model = Order
        fields = ['client', 'order_items']

    async def acreate(self, validated_data):
        items_data = validated_data.pop('order_items')

        # Create the order
        order = await Order.objects.acreate(**validated_data)

        # Add items to the order
        for item_data in items_data:
            item, created = await OrderItem.objects.aget_or_create(order=order, **item_data)

        return order


class OrderItemSerializer(ModelSerializer):
    class ProductSerializer2(ModelSerializer):
        class Meta:
            model = Product
            fields = ['title']

    product = ProductSerializer2()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'count', 'price']


class OrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(
        many=True, source='orderitem_set', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'datetime', 'published', 'order_items']
