from django.urls import path
from currency.views import LastRates, RateCSV

urlpatterns = [
    path('latest_rates', LastRates.as_view(), name='rates'),
    path('download/rates/', RateCSV.as_view(), name='download-rates'),

]
