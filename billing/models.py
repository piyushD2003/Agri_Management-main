from django.db import models
from django.conf import settings 
from users.models import Farm  
from master_data.models import Product

class Billing(models.Model):
    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE,
        related_name='billings'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name='billings'
    )
    bill_date = models.DateField(
        
    )    
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True
    )
    trader_name = models.CharField(
        max_length=255
    )  
    vehicle_number = models.CharField(
        max_length=255
    )  
    rate = models.FloatField(
        
    )
    trees = models.IntegerField(
        
    )
    leaves = models.IntegerField(
        
    )
    weight = models.FloatField(
        
    )
    total_amount = models.FloatField(
        
    )
    travelling_amount = models.FloatField(
        
    )
    final_amount = models.FloatField(
        
    )

    def __str__(self):
        return f"Billing {self.id} for {self.product.name} at {self.farm.name}"

    def save(self, *args, **kwargs):
        self.total_amount = self.rate * self.weight
        self.final_amount = self.total_amount + self.travelling_amount
        super(Billing, self).save(*args, **kwargs)
