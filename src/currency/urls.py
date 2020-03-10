from django.urls import path
from currency.views import LastRates

urlpatterns = [
    path('latest_rates', LastRates.as_view(), name='rates'),

]
