from rest_framework import serializers
from .models import ProductCategory
from .models import Product, City 


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__' 