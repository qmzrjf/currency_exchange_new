from django.http import HttpResponse
from django.views.generic import ListView, View, TemplateView
from currency.models import Rate
import csv
from urllib.parse import urlencode
from django_filters.views import FilterView
from currency.filters import RatesFilter
from currency import model_choices as mch
from django.core.cache import cache

from currency.utils import generate_rate_cache_key


class LastRates(FilterView):
    filterset_class = RatesFilter
    model = Rate
    template_name = 'last_rates.html'
    queryset = Rate.objects.all()
    paginate_by = 10


    def get_context_data(self, *args, **kwargs):

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

class LatestRates(TemplateView):
    template_name = "latest-rates.html"

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        rates = []
        for bank in mch.SOURCE_CHOICES:
            source = bank[0]
            for curr in mch.CURRENCY_CHOICES:
                currency = curr[0]

                cache_key = generate_rate_cache_key(source, currency)
                rate = cache.get(cache_key)
                if rate is None:
                    rate = Rate.objects.filter(source=source, currency=currency).order_by('created').last()
                    if rate:
                        rate_dict = {
                            'currency': rate.currency,
                            'source': rate.source,
                            'sale': rate.sale,
                            'buy': rate.buy,
                            'created': rate.created,
                        }
                        rates.append(rate_dict)
                        cache.set(cache_key, rate_dict, 60*15)
                else:
                    rates.append(rate)

        context["rates"] = rates

        return context
