from django.http import HttpResponse
from django.views.generic import ListView, View
from currency.models import Rate
import csv

class LastRates(ListView):
    model = Rate
    template_name = 'last_rates.html'
    queryset = Rate.objects.all()[:20]


class RateCSV(View):

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        writer = csv.writer(response)
        headers = [
            'id',
            'created',
            'currency',
            'source',
            'buy',
            'sale',
        ]
        writer.writerow(headers)
        for rate in Rate.objects.all().iterator():
            writer.writerow(map(str, [
                rate.id,
                rate.created,
                rate.get_currency_display(),
                rate.get_source_display(),
                rate.buy,
                rate.sale,
            ]))
        return response

