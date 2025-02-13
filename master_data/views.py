from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from master_data.models import ProductCategory, Product
from master_data.serializers import ProductCategorySerializer, ProductSerializer


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
            categories = ProductCategory.objects.all()
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
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Products!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get products!"}
            self.status = status.HTTP_404_NOT_FOUND

    def post(self, request):
        self.data = request.data
        self.pk = None

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "postCategory": self.postCategory,
                "postProduct": self.postProduct,
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
