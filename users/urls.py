from django.urls import path
from users.views import RegisterView, LoginView, UserAPI
from .views import FarmAPI


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', UserAPI.as_view(), name='users'),
    path('farms/', FarmAPI.as_view(), name='farms'),
   
]



    
