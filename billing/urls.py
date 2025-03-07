from django.urls import path
from .views import BillingAPI

urlpatterns = [
    path('billing/', BillingAPI.as_view(), name='billing_api'),
]
