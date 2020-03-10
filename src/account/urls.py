from django.urls import path
from account.views import MyProfile, ContactUs

urlpatterns = [
    path('profile/<int:pk>', MyProfile.as_view(), name='profile'),
    path('contact', ContactUs.as_view(), name='contact'),

]
