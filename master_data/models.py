from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ProductCategory(models.Model):
    name = models.CharField(
        max_length=255, unique=True
    )
    description = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    category = models.ForeignKey(
        ProductCategory, related_name='products',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        
        
# class City(models.Model):
#     name = models.CharField(
#         max_length=255, unique=True
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )
#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "City"
#         verbose_name_plural = "Cities"        

class Fertilizer(models.Model):
    name = models.CharField(
        max_length=255, unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    ) 
    price=models.FloatField(
        
    )
    
    def __str__(self):
        return self.name    
    

    
class SeedType(models.Model):
    name = models.CharField(
        max_length=255, unique=True
    )
    description = models.TextField(
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Seed Type"
        verbose_name_plural = "Seed Types"


class Seed(models.Model):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    seed_type = models.ForeignKey(
        SeedType, related_name='seeds',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Seed"
        verbose_name_plural = "Seeds"
    
class State(models.Model):
    name = models.CharField(
        max_length=255, unique=True
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='state_created', on_delete=models.SET_NULL, null=True
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='state_updated', on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"


class District(models.Model):
    name = models.CharField(
        max_length=255
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='district_created', on_delete=models.SET_NULL, null=True
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='district_updated', on_delete=models.SET_NULL, null=True
    )
    state = models.ForeignKey(
        State, related_name='districts', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"

class Taluka(models.Model):
    name = models.CharField(
        max_length=255
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='taluka_created', on_delete=models.SET_NULL, null=True
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='taluka_updated', on_delete=models.SET_NULL, null=True
    )
    district = models.ForeignKey(
        District, related_name='talukas', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Taluka"
        verbose_name_plural = "Talukas"


class Village(models.Model):
    name = models.CharField(
        max_length=255
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='village_created', on_delete=models.SET_NULL, null=True
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='village_updated', on_delete=models.SET_NULL, null=True
    )
    taluka = models.ForeignKey(
        Taluka, related_name='villages', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Village"
        verbose_name_plural = "Villages"