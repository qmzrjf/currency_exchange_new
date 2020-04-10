from django.urls import path
from currency.views import LastRates, RateCSV, LatestRates

urlpatterns = [
    path('rates', LastRates.as_view(), name='rates'),
    path('latest_rates', LatestRates.as_view(), name='latest-rates'),
    path('download/rates/', RateCSV.as_view(), name='download-rates'),

]
