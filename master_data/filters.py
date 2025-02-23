# filters.py
import django_filters
from master_data.models import ProductCategory, Product, City

# Filter for ProductCategory
class ProductCategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = ['name', 'description']

# Filter for Product
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    category_id = django_filters.NumberFilter(field_name='category__id')

    class Meta:
        model = Product
        fields = ['name', 'price', 'category_id']

# Filter for City
class CityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['name']
