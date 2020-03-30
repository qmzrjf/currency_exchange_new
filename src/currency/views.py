from django.http import HttpResponse
from django.views.generic import ListView, View
from currency.models import Rate
import csv

class LastRates(ListView):
    model = Rate
    template_name = 'last_rates.html'
    queryset = Rate.objects.all()


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

