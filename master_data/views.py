from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from master_data.models import ProductCategory, Product,Fertilizer, Seed, SeedType
from master_data.serializers import ProductCategorySerializer, ProductSerializer,FertilizerSerializer, SeedSerializer, SeedTypeSerializer
from master_data.filters import ProductCategoryFilter, ProductFilter, FertilizerFilter, SeedFilter, SeedTypeFilter
from .models import State, District, Taluka, Village
from .serializers import StateSerializer, DistrictSerializer, TalukaSerializer, VillageSerializer
from .filters import StateFilter, DistrictFilter, TalukaFilter, VillageFilter


class MasterData(APIView):

    def get(self, request):
        self.data = request.GET
        self.pk = None

        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "getCategory": self.getCategory,
                "getProduct": self.getProduct,
                "getfertilizer":self.getfertilizer,
                "getSeedType": self.getSeedType,  
                "getSeed": self.getSeed, 
                "getState": self.getState,
                "getDistrict": self.getDistrict,
                "getTaluka": self.getTaluka,
                "getVillage": self.getVillage,  
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status(request)
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def getCategory(self, request):
        try:
            category_filter = ProductCategoryFilter(request.GET, queryset=ProductCategory.objects.all())
            categories = category_filter.qs
            serializer = ProductCategorySerializer(categories, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Product Categories!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get categories!"}
            self.status = status.HTTP_404_NOT_FOUND

    def getProduct(self, request):
        try:
            # Apply filter for Product
            product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
            products = product_filter.qs
            serializer = ProductSerializer(products, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Products!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get products!"}
            self.status = status.HTTP_404_NOT_FOUND

   
    
    def getfertilizer(self, request):
        try:
            # Apply filter for Fertilizer
            fertilizer_filter = FertilizerFilter(request.GET, queryset=Fertilizer.objects.all())
            fertilizers = fertilizer_filter.qs
            serializer = FertilizerSerializer(fertilizers, many=True).data
            
            if self.pk and len(serializer):
                serializer = serializer[0]
            
            self.ctx = {"message": "Successfully retrieved Fertilizers!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get fertilizers!"}
            self.status = status.HTTP_404_NOT_FOUND
        
    def getSeedType(self, request):
        try:
            seed_type_filter = SeedTypeFilter(request.GET, queryset=SeedType.objects.all())
            seed_types = seed_type_filter.qs
            serializer = SeedTypeSerializer(seed_types, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Seed Types!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get seed types!"}
            self.status = status.HTTP_404_NOT_FOUND

    def getSeed(self, request):
        try:
            seed_filter = SeedFilter(request.GET, queryset=Seed.objects.all())
            seeds = seed_filter.qs
            serializer = SeedSerializer(seeds, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Seeds!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get seeds!"}
            self.status = status.HTTP_404_NOT_FOUND   

    def getState(self, request):
        try:
            state_filter = StateFilter(request.GET, queryset=State.objects.all())
            states = state_filter.qs
            serializer = StateSerializer(states, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved States!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get states!"}
            self.status = status.HTTP_404_NOT_FOUND

    def getDistrict(self, request):
        try:
            district_filter = DistrictFilter(request.GET, queryset=District.objects.all())
            districts = district_filter.qs
            serializer = DistrictSerializer(districts, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Districts!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get districts!"}
            self.status = status.HTTP_404_NOT_FOUND

    def getTaluka(self, request):
        try:
            taluka_filter = TalukaFilter(request.GET, queryset=Taluka.objects.all())
            talukas = taluka_filter.qs
            serializer = TalukaSerializer(talukas, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Talukas!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get talukas!"}
            self.status = status.HTTP_404_NOT_FOUND

    def getVillage(self, request):
        try:
            village_filter = VillageFilter(request.GET, queryset=Village.objects.all())
            villages = village_filter.qs
            serializer = VillageSerializer(villages, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Villages!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get villages!"}
            self.status = status.HTTP_404_NOT_FOUND        

    def post(self, request):
        self.data = request.data
        self.pk = None

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "postCategory": self.postCategory,
                "postProduct": self.postProduct,
                "postfertilizer":self.postfertilizer,
                "postSeedType": self.postSeedType, 
                "postSeed": self.postSeed,
                "postState": self.postState,
                "postDistrict": self.postDistrict,
                "postTaluka": self.postTaluka,
                "postVillage": self.postVillage, 
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def postCategory(self):
        name = self.data.get("name")
        description = self.data.get("description")

        try:
            obj = ProductCategory(name=name, description=description)
            obj.save()
            serializer = ProductCategorySerializer(obj).data
            self.ctx = {"message": "Product Category Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def postProduct(self):
        name = self.data.get("name")
        description = self.data.get("description")
        price = self.data.get("price")
        category_id = self.data.get("category_id")

        try:
            
            category = ProductCategory.objects.get(id=category_id)
            product = Product(name=name, description=description, price=price, category=category)
            product.save()
            serializer = ProductSerializer(product).data
            self.ctx = {"message": "Product Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except ProductCategory.DoesNotExist:
            self.ctx = {"message": "Category not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


    def postfertilizer(self):
        name = self.data.get("name")
        price = self.data.get("price")

        if not name or not price:
            self.ctx = {"message": "Missing required fields: name or price!"}
            self.status = status.HTTP_400_BAD_REQUEST
            return
        try:
            
            fertilizer = Fertilizer(name=name, price=price)
            fertilizer.save() 
            serializer = FertilizerSerializer(fertilizer).data
            self.ctx = {"message": "Fertilizer Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def postSeedType(self):
        name = self.data.get("name")
        description = self.data.get("description")

        try:
            seed_type = SeedType(name=name, description=description)
            seed_type.save()
            serializer = SeedTypeSerializer(seed_type).data
            self.ctx = {"message": "Seed Type Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def postSeed(self):
        name = self.data.get("name")
        description = self.data.get("description")
        price = self.data.get("price")
        seed_type_id = self.data.get("seed_type_id")

        try:
            seed_type = SeedType.objects.get(id=seed_type_id)
            seed = Seed(name=name, description=description, price=price, seed_type=seed_type)
            seed.save()
            serializer = SeedSerializer(seed).data
            self.ctx = {"message": "Seed Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except SeedType.DoesNotExist:
            self.ctx = {"message": "Seed Type not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


    def postState(self):
        name = self.data.get("name")
        try:
            state = State(name=name)
            state.save()
            serializer = StateSerializer(state).data
            self.ctx = {"message": "State Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def postDistrict(self):
        name = self.data.get("name")
        state_id = self.data.get("state_id")
        try:
            state = State.objects.get(id=state_id)
            district = District(name=name, state=state)
            district.save()
            serializer = DistrictSerializer(district).data
            self.ctx = {"message": "District Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except State.DoesNotExist:
            self.ctx = {"message": "State not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def postTaluka(self):
        name = self.data.get("name")
        district_id = self.data.get("district_id")
        try:
            district = District.objects.get(id=district_id)
            taluka = Taluka(name=name, district=district)
            taluka.save()
            serializer = TalukaSerializer(taluka).data
            self.ctx = {"message": "Taluka Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except District.DoesNotExist:
            self.ctx = {"message": "District not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def postVillage(self):
        name = self.data.get("name")
        taluka_id = self.data.get("taluka_id")
        try:
            taluka = Taluka.objects.get(id=taluka_id)
            village = Village(name=name, taluka=taluka)
            village.save()
            serializer = VillageSerializer(village).data
            self.ctx = {"message": "Village Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Taluka.DoesNotExist:
            self.ctx = {"message": "Taluka not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        

    def patch(self, request):
        self.data = request.data
        self.pk = None

        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "patchCategory": self.patchCategory,
                "patchProduct": self.patchProduct,
                "patchfertilizer":self.patchfertilizer,
                "patchSeedType": self.patchSeedType,  
                "patchSeed": self.patchSeed, 
                "patchState": self.patchState,
                "patchDistrict": self.patchDistrict,
                "patchTaluka": self.patchTaluka,
                "patchVillage": self.patchVillage,  
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def patchCategory(self):
        name = self.data.get("name")
        description = self.data.get("description")

        try:
            category = ProductCategory.objects.get(pk=self.pk)

            if name:
                category.name = name
            if description:
                category.description = description

            category.save()

            serializer = ProductCategorySerializer(category).data
            self.ctx = {"message": "Product Category Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except ProductCategory.DoesNotExist:
            self.ctx = {"message": f"Product Category with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def patchProduct(self):
        name = self.data.get("name")
        description = self.data.get("description")
        price = self.data.get("price")
        category_id = self.data.get("category_id")

        try:
            product = Product.objects.get(pk=self.pk)
            if name:
                product.name = name
            if description:
                product.description = description
            if price:
                product.price = price
            if category_id:
                category = ProductCategory.objects.get(id=category_id)
                product.category = category

            product.save()
            serializer = ProductSerializer(product).data
            self.ctx = {"message": "Product Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Product.DoesNotExist:
            self.ctx = {"message": "Product not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

            
    def patchfertilizer(self):
        name = self.data.get("name")
        price = self.data.get("price")

        try:
            fertilizer = Fertilizer.objects.get(pk=self.pk)

            if name:
                fertilizer.name = name
            if price is not None:  
                fertilizer.price = price
            fertilizer.save()

            serializer = FertilizerSerializer(fertilizer).data
            self.ctx = {"message": "Fertilizer Updated!", "data": serializer}
            self.status = status.HTTP_200_OK

        except Fertilizer.DoesNotExist:
            self.ctx = {"message": f"Fertilizer with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def patchSeedType(self):
        name = self.data.get("name")
        description = self.data.get("description")

        try:
            seed_type = SeedType.objects.get(pk=self.pk)

            if name:
                seed_type.name = name
            if description:
                seed_type.description = description

            seed_type.save()

            serializer = SeedTypeSerializer(seed_type).data
            self.ctx = {"message": "Seed Type Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except SeedType.DoesNotExist:
            self.ctx = {"message": f"Seed Type with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def patchSeed(self):
        name = self.data.get("name")
        description = self.data.get("description")
        price = self.data.get("price")
        seed_type_id = self.data.get("seed_type_id")

        try:
            seed = Seed.objects.get(pk=self.pk)
            if name:
                seed.name = name
            if description:
                seed.description = description
            if price:
                seed.price = price
            if seed_type_id:
                seed_type = SeedType.objects.get(id=seed_type_id)
                seed.seed_type = seed_type

            seed.save()
            serializer = SeedSerializer(seed).data
            self.ctx = {"message": "Seed Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Seed.DoesNotExist:
            self.ctx = {"message": "Seed not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR   


    def patchState(self):
        name = self.data.get("name")
        
        try:
            state = State.objects.get(pk=self.pk)

            if name:
                state.name = name
            
            state.save()

            serializer = StateSerializer(state).data
            self.ctx = {"message": "State Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except State.DoesNotExist:
            self.ctx = {"message": f"State with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def patchDistrict(self):
        name = self.data.get("name")
        state_id = self.data.get("state_id")
        
        try:
            district = District.objects.get(pk=self.pk)

            if name:
                district.name = name
            if state_id:
                state = State.objects.get(id=state_id)
                district.state = state
            
            district.save()

            serializer = DistrictSerializer(district).data
            self.ctx = {"message": "District Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except District.DoesNotExist:
            self.ctx = {"message": f"District with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except State.DoesNotExist:
            self.ctx = {"message": f"State with id {state_id} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def patchTaluka(self):
        name = self.data.get("name")
        district_id = self.data.get("district_id")
        
        try:
            taluka = Taluka.objects.get(pk=self.pk)

            if name:
                taluka.name = name
            if district_id:
                district = District.objects.get(id=district_id)
                taluka.district = district
            
            taluka.save()

            serializer = TalukaSerializer(taluka).data
            self.ctx = {"message": "Taluka Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Taluka.DoesNotExist:
            self.ctx = {"message": f"Taluka with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except District.DoesNotExist:
            self.ctx = {"message": f"District with id {district_id} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def patchVillage(self):
        name = self.data.get("name")
        taluka_id = self.data.get("taluka_id")
        
        try:
            village = Village.objects.get(pk=self.pk)

            if name:
                village.name = name
            if taluka_id:
                taluka = Taluka.objects.get(id=taluka_id)
                village.taluka = taluka
            
            village.save()

            serializer = VillageSerializer(village).data
            self.ctx = {"message": "Village Updated!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Village.DoesNotExist:
            self.ctx = {"message": f"Village with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Taluka.DoesNotExist:
            self.ctx = {"message": f"Taluka with id {taluka_id} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
         

    def delete(self, request):
        self.data = request.data
        self.pk = None

        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "deleteCategory": self.deleteCategory,
                "deleteProduct": self.deleteProduct,
                "deletefertilizer":self.deletefertilizer,
                "deleteSeedType": self.deleteSeedType, 
                "deleteSeed": self.deleteSeed,
                "deleteState": self.deleteState,
                "deleteDistrict": self.deleteDistrict,
                "deleteTaluka": self.deleteTaluka,
                "deleteVillage": self.deleteVillage,
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def deleteCategory(self):
        try:
            category = ProductCategory.objects.get(pk=self.pk)
            category.delete()
            self.ctx = {"message": "Product Category Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except ProductCategory.DoesNotExist:
            self.ctx = {"message": "Product Category not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def deleteProduct(self):
        try:
            product = Product.objects.get(pk=self.pk)
            product.delete()
            self.ctx = {"message": "Product Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except Product.DoesNotExist:
            self.ctx = {"message": "Product not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def deletefertilizer(self):
        try:
            fertilizer = Fertilizer.objects.get(pk=self.pk)
            
            fertilizer.delete()

            self.ctx = {"message": "Fertilizer Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT

        except Fertilizer.DoesNotExist:
            self.ctx = {"message": f"Fertilizer with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND

        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            
            
    def deleteSeedType(self):
        try:
            seed_type = SeedType.objects.get(pk=self.pk)
            seed_type.delete()
            self.ctx = {"message": "Seed Type Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except SeedType.DoesNotExist:
            self.ctx = {"message": "Seed Type not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def deleteSeed(self):
        try:
            seed = Seed.objects.get(pk=self.pk)
            seed.delete()
            self.ctx = {"message": "Seed Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except Seed.DoesNotExist:
            self.ctx = {"message": "Seed not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR        

    def deleteState(self):
        try:
            state = State.objects.get(pk=self.pk)
            state.delete()
            self.ctx = {"message": "State Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except State.DoesNotExist:
            self.ctx = {"message": f"State with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def deleteDistrict(self):
        try:
            district = District.objects.get(pk=self.pk)
            district.delete()
            self.ctx = {"message": "District Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except District.DoesNotExist:
            self.ctx = {"message": f"District with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def deleteTaluka(self):
        try:
            taluka = Taluka.objects.get(pk=self.pk)
            taluka.delete()
            self.ctx = {"message": "Taluka Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except Taluka.DoesNotExist:
            self.ctx = {"message": f"Taluka with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def deleteVillage(self):
        try:
            village = Village.objects.get(pk=self.pk)
            village.delete()
            self.ctx = {"message": "Village Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except Village.DoesNotExist:
            self.ctx = {"message": f"Village with id {self.pk} not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
