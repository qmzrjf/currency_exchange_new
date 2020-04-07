import django_filters

from currency.models import Rate

class RatesFilter(django_filters.FilterSet):
    created_date = django_filters.DateFilter(field_name='created', lookup_expr='date')
    class Meta:
        model = Rate
        fields = ['sale', 'buy', 'source', 'created_date']