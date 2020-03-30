from django.urls import path
from currency.api.views import RatesView, RateView



app_name = 'api-currency'
urlpatterns = [
    path('rates/', RatesView.as_view(), name='rates'),
    path('rates/<int:pk>', RateView.as_view(), name='rate'),


]
