from django.urls import path
from .views import MasterData

urlpatterns = [
    path('', MasterData.as_view(), name='master_data'),
]
