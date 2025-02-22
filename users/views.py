from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import User
from users.serializers import (
    LoginSerializer,
    UserSerializer
)
from .serializers import FarmerSerializer, FarmManagerSerializer
from .models import Farmer, FarmManager
from .serializers import FarmSerializer
from .models import Farm 
from .models import City 


class RegisterView(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not first_name or not last_name or not email or not phone or not password:
            return Response({'error': 'Please provide all required fields.'},  status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone=phone).exists():
            return Response({'error': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )

        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        user_data = UserSerializer(user).data
        user_data['access'] = access_token
        user_data['refresh'] = refresh_token
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPI(APIView):
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        self.data = request.GET
        self.pk = None    
        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])
                   
            action_mapper = {
                 "getUser": self.getUser,
                
            }
            action_status = action_mapper.get(action)
            if action_status:
                
                action_status(request)
            else:
                return Response({"message": "Choose Wrong Option !", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa
            
    def getUser(self, request):
        try:
            
            data = User.objects.all()
            serializer = UserSerializer(data, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            
            self.ctx = {"message": "Successfully getting User!", "data": serializer}  # noqa
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Not getting data!"}
            self.status = status.HTTP_404_NOT_FOUND
               
    def post(self, request):
            self.data = request.data
            self.pk = None
            self.user = request.user
            if not request.user.is_authenticated:
                return Response({"message": "Authentication credentials were not provided."},
                                status=status.HTTP_401_UNAUTHORIZED)
            if "id" in self.data:
                self.pk = self.data.get("id")

            if "action" in self.data:
                action = str(self.data["action"])
                action_mapper = {
                    "postUser": self.postUser,
                   
                }
                
                action_status = action_mapper.get(action)
                if action_status:
                    action_status()
                else:
                    return Response({"message": "Choose Wrong Option !", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa
                return Response(self.ctx, self.status)
            else:
                return Response({"message": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa   
                   
    def postUser(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        email = self.data.get("email")
        phone = self.data.get("phone")

        try:
           
            obj = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
            obj.save()
            serializer = UserSerializer(obj).data
            self.ctx = {"message": "User is Created!", "data": serializer}  
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def patch(self, request):   
        self.data = request.data
        self.pk = None
        self.user = request.user
        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        if "id" in self.data:
            self.id = self.data["id"]

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "patchUser": self.patchUser,
               
                
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option !", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa
           
    def patchUser(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        email = self.data.get("email")
        phone = self.data.get("phone")

        try:
            
            user = User.objects.get(pk=self.id)  

            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if phone:
                user.phone = phone
            if email:
                user.email = email
            
            user.save()  

            serializer = UserSerializer(user).data
            self.ctx = {"message": "User is Updated!", "data": serializer}
            self.status = status.HTTP_200_OK 
        except User.DoesNotExist:
          
            self.ctx = {"message": f"User with id {self.id} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
           
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
                
    def delete(self, request):     
        self.data = request.data
        self.pk = None
        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        if "id" in self.data:
            self.id = self.data["id"]

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "delUser": self.delUser,
                
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option !", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST) # noqa
            
    def delUser(self):
        try:
            data = User.objects.get(pk=self.id)
            if data:
                data.delete()
            self.ctx = {"message": "User deleted!"}
            self.status = status.HTTP_201_CREATED
        except User.DoesNotExist:
            self.ctx = {"message": "User id Not Found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR                    
            
         
class FarmAPI(APIView):

    def get(self, request):
        self.data = request.GET
        self.pk = None

        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                    "getFarmer": self.getFarmer,
                    "getFarmManager": self.getFarmManager,
                    "getFarm": self.getFarm,  
            }

            action_status = action_mapper.get(action)
            if action_status:
                action_status()  # No need to pass request here
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

        
    def getFarmer(self):
        try:
            data = Farmer.objects.all()
            serializer = FarmerSerializer(data, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully fetched Farmer data!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Error fetching data!"}
            self.status = status.HTTP_404_NOT_FOUND

    def getFarmManager(self):
        try:
            data = FarmManager.objects.all()
            serializer = FarmManagerSerializer(data, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully fetched Farm Manager data!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Error fetching data!"}
            self.status = status.HTTP_404_NOT_FOUND
            
    def getFarm(self):
        try:
            data = Farm.objects.all()
            serializer = FarmSerializer(data, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully fetched Farm data!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Error fetching data!"}
            self.status = status.HTTP_404_NOT_FOUND
   
            
    def post(self, request):
        self.data = request.data
        self.pk = None

        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if "action" in self.data:
            action = str(self.data["action"])

            action_mapper = {
                
                    "postFarmer": self.postFarmer,
                    "postFarmManager": self.postFarmManager,
                    "postFarm": self.postFarm,    
            }

            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def postFarmer(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        email = self.data.get("email")
        phone = self.data.get("phone")
        farm_name = self.data.get("farm_name")
        farm_location = self.data.get("farm_location")
        farm_size = self.data.get("farm_size")

        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )

            farmer = Farmer(
                user=user,
                farm_name=farm_name,
                farm_location=farm_location,
                farm_size=farm_size
            )
            farmer.save()

            serializer = FarmerSerializer(farmer).data
            self.ctx = {"message": "Farmer is Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def postFarmManager(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        email = self.data.get("email")
        phone = self.data.get("phone")
        farm_name = self.data.get("farm_name")
        farm_location = self.data.get("farm_location")
        manager_experience = self.data.get("manager_experience")

        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )

            farm_manager = FarmManager(
                user=user,
                farm_name=farm_name,
                farm_location=farm_location,
                manager_experience=manager_experience
            )
            farm_manager.save()

            serializer = FarmManagerSerializer(farm_manager).data
            self.ctx = {"message": "Farm Manager is Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            
    def postFarm(self):
        farm_name = self.data.get("farm_name")
        address = self.data.get("address")
        location_url = self.data.get("location_url")
        city_id = self.data.get("city") 
        farm_size = self.data.get("farm_size")

        try:
           

         
            city = City.objects.get(id=city_id)

            
            farm = Farm.objects.create(
                name=farm_name,
                address=address,
                location_url=location_url,
                city=city,
                farm_size=farm_size,
                user_created=self.request.user 
            )

          
            serializer = FarmSerializer(farm).data
            self.ctx = {"message": "Farm is Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except City.DoesNotExist:
            self.ctx = {"message": "City not found", "data": None}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(self.ctx, status=self.status)
    def patch(self, request):
        self.data = request.data
        self.pk = None

        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])

            action_mapper = {
                
                    "patchFarmer": self.patchFarmer,
                    "patchFarmManager": self.patchFarmManager,
                    "patchFarm": self.patchFarm,  
               
            }

            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def patchFarmer(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        email = self.data.get("email")
        phone = self.data.get("phone")
        farm_name = self.data.get("farm_name")
        farm_location = self.data.get("farm_location")
        farm_size = self.data.get("farm_size")

        try:
            
            user = User.objects.get(id=self.pk)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone = phone
            user.save()
            farmer = Farmer.objects.get(user=user)
            farmer.farm_name = farm_name
            farmer.farm_location = farm_location
            farmer.farm_size = farm_size
            farmer.save()

            serializer = FarmerSerializer(farmer).data
            self.ctx = {"message": "Farmer is Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except User.DoesNotExist:
            self.ctx = {"message": "User not found", "data": None}
            self.status = status.HTTP_404_NOT_FOUND
        except Farmer.DoesNotExist:
            self.ctx = {"message": "Farmer not found", "data": None}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            
    def patchFarmManager(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        email = self.data.get("email")
        phone = self.data.get("phone")
        farm_name = self.data.get("farm_name")
        farm_location = self.data.get("farm_location")
        manager_experience = self.data.get("manager_experience")

        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )

            farm_manager = FarmManager(
                user=user,
                farm_name=farm_name,
                farm_location=farm_location,
                manager_experience=manager_experience
            )
            farm_manager.save()

            serializer = FarmManagerSerializer(farm_manager).data
            self.ctx = {"message": "Farm Manager is Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            
            
    def patchFarm(self):
        farm_name = self.data.get("farm_name")
        address = self.data.get("address")
        location_url = self.data.get("location_url")
        farm_size = self.data.get("farm_size")
        city_id = self.data.get("city")  

        try:
           
            farm = Farm.objects.get(pk=self.pk)

            
            if farm_name:
                farm.name = farm_name
            if address:
                farm.address = address
            if location_url:
                farm.location_url = location_url
            if farm_size:
                farm.farm_size = farm_size

            
            if city_id:
                try:
                    city = City.objects.get(id=city_id)
                    farm.city = city
                except City.DoesNotExist:
                    self.ctx = {"message": "City with the provided ID not found", "data": None}
                    self.status = status.HTTP_404_NOT_FOUND
                    return  

            
            farm.save()

           
            serializer = FarmSerializer(farm).data
            self.ctx = {"message": "Farm is Updated!", "data": serializer}
            self.status = status.HTTP_200_OK

        except Farm.DoesNotExist:
            self.ctx = {"message": "Farm not found", "data": None}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

            

    def delete(self, request):
        self.data = request.data
        self.pk = None

        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])

            action_mapper = {
                
                    "delFarmer": self.delFarmer,
                    "delFarmManager": self.delFarmManager,
                    "delFarm": self.delFarm,  
              
            }

            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def delFarmer(self):
        try:
            farmer = Farmer.objects.get(pk=self.pk)
            user = farmer.user
            farmer.delete()
            user.delete()
            self.ctx = {"message": "Farmer deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except Farmer.DoesNotExist:
            self.ctx = {"message": "Farmer id Not Found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def delFarmManager(self):
        try:
            farm_manager = FarmManager.objects.get(pk=self.pk)
            user = farm_manager.user
            farm_manager.delete()
            user.delete()
            self.ctx = {"message": "Farm Manager deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except FarmManager.DoesNotExist:
            self.ctx = {"message": "Farm Manager id Not Found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def delFarm(self):
        try:
            farm = Farm.objects.get(pk=self.pk)
            farm.delete()
            self.ctx = {"message": "Farm deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except Farm.DoesNotExist:
            self.ctx = {"message": "Farm id Not Found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR