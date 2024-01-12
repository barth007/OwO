from django.urls import path
from .views import AboutUs



urlpatterns = [ 
    path('about-us/', AboutUs.as_view(), name='about-us'),
]