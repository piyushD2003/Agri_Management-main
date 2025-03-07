from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from users.models import User, Farmer, FarmManager,Farm


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            user = authenticate(request=self.context.get('request'), phone=phone, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid phone number or password.')
            if not user.is_active:
                raise serializers.ValidationError('This account is inactive.')
        else:
            raise serializers.ValidationError('Must include "phone" and "password".')

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  
           
  
class FarmerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  
    
    class Meta:
        model = Farmer
        fields = ['id', 'user', 'farm_name', 'farm_location', 'farm_size']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        farmer = Farmer.objects.create(user=user, **validated_data)
        return farmer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.phone = user_data.get('phone', user.phone)
        user.save()   
        instance.farm_name = validated_data.get('farm_name', instance.farm_name)
        instance.farm_location = validated_data.get('farm_location', instance.farm_location)
        instance.farm_size = validated_data.get('farm_size', instance.farm_size)
        instance.save()
        
        return instance    
    
    
class FarmManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FarmManager
        fields = ['id', 'user', 'farm_name', 'farm_location', 'manager_experience']
           
    def create(self, validated_data):
        """ Custom create method to handle nested user creation """
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        farm_manager = FarmManager.objects.create(user=user, **validated_data)
        return farm_manager

    def update(self, instance, validated_data):
        
        user_data = validated_data.pop('user')
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.phone = user_data.get('phone', user.phone)
        user.save()
        instance.farm_name = validated_data.get('farm_name', instance.farm_name)
        instance.farm_location = validated_data.get('farm_location', instance.farm_location)
        instance.manager_experience = validated_data.get('manager_experience', instance.manager_experience)
        instance.save()
        return instance
                            
                            
class FarmSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Farm
        fields = ['name', 'address', 'location_url', 'farm_size','id']

    # def get_city_name(self, obj):
    #     return obj.city.name if obj.city else None