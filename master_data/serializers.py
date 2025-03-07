from rest_framework import serializers
from .models import ProductCategory
from .models import Product,Fertilizer
from .models import Seed,SeedType,State, District, Taluka, Village

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category']
   
class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = '__all__'        
        
class SeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seed
        fields = '__all__'  

class SeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedType
        fields = '__all__'  
        

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']  


class DistrictSerializer(serializers.ModelSerializer):
    state = StateSerializer() 
    class Meta:
        model = District
        fields = ['id', 'name', 'state']


class TalukaSerializer(serializers.ModelSerializer):
    district = DistrictSerializer() 

    class Meta:
        model = Taluka
        fields = ['id', 'name', 'district']


class VillageSerializer(serializers.ModelSerializer):
    taluka = TalukaSerializer()  

    class Meta:
        model = Village
        fields = ['id', 'name', 'taluka']        