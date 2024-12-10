from rest_framework import serializers
from adrf.serializers import Serializer, ModelSerializer
from app.models import *
from bot.models import Bot_user


class ProductSerializer(ModelSerializer):
    price_for_client = serializers.CharField()

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='id'
    )
    class Meta:
        model = OrderItem
        fields = ['product', 'count']


class OrderSerializer(ModelSerializer):
    client = serializers.SlugRelatedField(
        queryset=Client.objects.all(),
        slug_field='id'
    )
    order_items = OrderItemSerializer(many=True)

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
