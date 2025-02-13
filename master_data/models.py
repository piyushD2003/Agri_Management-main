from django.db import models


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
