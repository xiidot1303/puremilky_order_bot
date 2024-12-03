from rest_framework import serializers
from adrf.serializers import Serializer, ModelSerializer
from app.models import *
from bot.models import Bot_user


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
