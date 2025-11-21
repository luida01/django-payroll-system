from django_filters import rest_framework as filters
from .models import Employee

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class EmployeeFilter(filters.FilterSet):
    min_salary = filters.NumberFilter(field_name="salary", lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name="salary", lookup_expr='lte')
    
    institutions = NumberInFilter(field_name='institution', lookup_expr='in')
    departments = NumberInFilter(field_name='department', lookup_expr='in')
    positions = NumberInFilter(field_name='position', lookup_expr='in')
    
    hire_date_from = filters.DateFilter(field_name='hire_date', lookup_expr='gte')
    hire_date_to = filters.DateFilter(field_name='hire_date', lookup_expr='lte')

    class Meta:
        model = Employee
        fields = ['is_active']
