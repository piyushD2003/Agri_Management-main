from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Billing
from .serializers import BillingSerializer  
from users.models import Farm
from master_data.models import Product
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model


class BillingAPI(APIView):    
    def get(self, request):
        self.data = request.GET
        self.pk = None

        if "id" in self.data:
            self.pk = self.data.get("id")

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "getBilling": self.getBilling,
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status(request)
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def getBilling(self, request):
        try:
            billing_filter = Billing.objects.all()
            if self.pk:
                billing_filter = billing_filter.filter(id=self.pk)
            serializer = BillingSerializer(billing_filter, many=True).data
            if self.pk and len(serializer):
                serializer = serializer[0]
            self.ctx = {"message": "Successfully retrieved Billing!", "data": serializer}
            self.status = status.HTTP_200_OK
        except Exception:
            self.ctx = {"message": "Failed to get billing!"}
            self.status = status.HTTP_404_NOT_FOUND

    def post(self, request):
        self.data = request.data
        self.pk = None

        if "action" in self.data:
            action = str(self.data["action"])
            action_mapper = {
                "postBilling": self.postBilling,
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def postBilling(self):
        farm_id = self.data.get("farm_id")
        product_id = self.data.get("product_id")
        bill_date = self.data.get("bill_date")
        user_created_id = self.data.get("user_created_id")
        trader_name = self.data.get("trader_name")
        vehicle_number = self.data.get("vehicle_number")
        rate = self.data.get("rate")
        trees = self.data.get("trees")
        leaves = self.data.get("leaves")
        weight = self.data.get("weight")
        travelling_amount = self.data.get("travelling_amount")

        try:
            farm = Farm.objects.get(id=farm_id)
            product = Product.objects.get(id=product_id)
            User = get_user_model()
            user_created = User.objects.get(id=user_created_id)

            total_amount = rate * weight
            final_amount = total_amount + travelling_amount

            billing = Billing(
                farm=farm,
                product=product,
                bill_date=bill_date,
                user_created=user_created,
                trader_name=trader_name,
                vehicle_number=vehicle_number,
                rate=rate,
                trees=trees,
                leaves=leaves,
                weight=weight,
                total_amount=total_amount,
                travelling_amount=travelling_amount,
                final_amount=final_amount
            )
            billing.save()

            serializer = BillingSerializer(billing).data
            self.ctx = {"message": "Billing Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Farm.DoesNotExist:
            self.ctx = {"message": "Farm not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Product.DoesNotExist:
            self.ctx = {"message": "Product not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except User.DoesNotExist:
            self.ctx = {"message": "User not found!"}
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
                "patchBilling": self.patchBilling,
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def patchBilling(self):
        farm_id = self.data.get("farm_id")
        product_id = self.data.get("product_id")
        bill_date = self.data.get("bill_date")
        user_created_id = self.data.get("user_created_id")
        trader_name = self.data.get("trader_name")
        vehicle_number = self.data.get("vehicle_number")
        rate = self.data.get("rate")
        trees = self.data.get("trees")
        leaves = self.data.get("leaves")
        weight = self.data.get("weight")
        travelling_amount = self.data.get("travelling_amount")

        try:
            farm = Farm.objects.get(id=farm_id)
            product = Product.objects.get(id=product_id)
            User = get_user_model()
            user_created = User.objects.get(id=user_created_id)

            total_amount = rate * weight
            final_amount = total_amount + travelling_amount

            billing = Billing(
                farm=farm,
                product=product,
                bill_date=bill_date,
                user_created=user_created,
                trader_name=trader_name,
                vehicle_number=vehicle_number,
                rate=rate,
                trees=trees,
                leaves=leaves,
                weight=weight,
                total_amount=total_amount,
                travelling_amount=travelling_amount,
                final_amount=final_amount
            )
            billing.save()

            serializer = BillingSerializer(billing).data
            self.ctx = {"message": "Billing Created!", "data": serializer}
            self.status = status.HTTP_201_CREATED
        except Farm.DoesNotExist:
            self.ctx = {"message": "Farm not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Product.DoesNotExist:
            self.ctx = {"message": "Product not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except User.DoesNotExist:
            self.ctx = {"message": "User not found!"}
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
                "deleteBilling": self.deleteBilling,
            }
            action_status = action_mapper.get(action)
            if action_status:
                action_status()
            else:
                return Response({"message": "Choose Wrong Option!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.ctx, self.status)
        else:
            return Response({"message": "Action is not in dict", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def deleteBilling(self):
        try:
            billing = Billing.objects.get(pk=self.pk)
            billing.delete()
            self.ctx = {"message": "Billing Deleted!"}
            self.status = status.HTTP_204_NO_CONTENT
        except Billing.DoesNotExist:
            self.ctx = {"message": "Billing not found!"}
            self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"message": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
