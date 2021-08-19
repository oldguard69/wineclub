import django_filters
from customer.models import Customer

class CustomerFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter('is_active', 'exact')
    fullname = django_filters.CharFilter('fullname', 'icontains')
    phone = django_filters.CharFilter('phone_number', 'icontains')

    # class Meta:
    #     model = Customer
    #     fields = ('is_active', 'fullname', 'phone_name')