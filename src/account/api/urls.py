from django.urls import path
from account.api.views import ContactsView, ContactView



app_name = 'api-account'
urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/<int:pk>', ContactView.as_view(), name='contact'),


]
