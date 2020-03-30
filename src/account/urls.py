from django.urls import path
from account.views import MyProfile, ContactUs, SignUpView, Activate

urlpatterns = [
    path('profile/<int:pk>', MyProfile.as_view(), name='profile'),
    path('contact/', ContactUs.as_view(), name='contact'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uuid:activation_code>/', Activate.as_view(), name='activate'),

]
