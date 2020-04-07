from django.http import HttpResponse
from django.views.generic import ListView, View
from currency.models import Rate
import csv

from django_filters.views import FilterView
from currency.filters import RatesFilter

class LastRates(FilterView):
    filterset_class = RatesFilter
    model = Rate
    template_name = 'last_rates.html'
    queryset = Rate.objects.all()
    paginate_by = 10


    def get_context_data(self, *args, **kwargs):
        from urllib.parse import urlencode
        context = super().get_context_data(*args, **kwargs)
        query_params = dict(self.request.GET.items())
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = urlencode(query_params)


        return context


class RateCSV(View):
    HEADERS = [
        'id',
        'created',
        'source',
        'currency',
        'buy',
        'sale',

    ]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        writer = csv.writer(response)

        writer.writerow(self.HEADERS)

        for rate in Rate.objects.all().iterator():
            row = [
                getattr(rate, f'get_{attr}_display')()
                if hasattr(rate, f'get_{attr}_display') else getattr(rate, attr)
                for attr in self.HEADERS
            ]
            writer.writerow(row)

        return response
