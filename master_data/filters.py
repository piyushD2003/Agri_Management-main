
import django_filters
from master_data.models import ProductCategory, Product,Fertilizer, Seed, SeedType
from .models import State, District, Taluka, Village



class ProductCategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = ['name', 'description']


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    category_id = django_filters.NumberFilter(field_name='category__id')

    class Meta:
        model = Product
        fields = ['name', 'price', 'category_id']
        
        
class FertilizerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # Filter by name (case insensitive)

    class Meta:
        model = Fertilizer
        fields = ['name']        


class SeedFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  
    price = django_filters.NumberFilter()  
    seed_type = django_filters.ModelChoiceFilter(queryset=SeedType.objects.all(), required=False)  

    class Meta:
        model = Seed
        fields = ['name', 'price', 'seed_type'] 


class SeedTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  

    class Meta:
        model = SeedType
        fields = ['name']


class StateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = State
        fields = ['name']

class DistrictFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.ModelChoiceFilter(queryset=State.objects.all())

    class Meta:
        model = District
        fields = ['name', 'state']

class TalukaFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    district = django_filters.ModelChoiceFilter(queryset=District.objects.all())

    class Meta:
        model = Taluka
        fields = ['name', 'district']

class VillageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    taluka = django_filters.ModelChoiceFilter(queryset=Taluka.objects.all())

    class Meta:
        model = Village
        fields = ['name', 'taluka']