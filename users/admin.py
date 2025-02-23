from django.contrib import admin
from .models import User, Farmer, FarmManager, Farm 


admin.site.register(User)
admin.site.register(Farmer)
admin.site.register(FarmManager)
admin.site.register(Farm)  
