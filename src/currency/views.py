from django.views.generic import ListView
from currency.models import Rate


class LastRates(ListView):
    model = Rate
    template_name = 'last_rates.html'
    queryset = Rate.objects.all()[:20]
