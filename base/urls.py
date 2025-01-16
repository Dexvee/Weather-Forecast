from django.urls import path
from .views import home_view, forecast_view

urlpatterns = [
    path('', home_view, name='home'),
    path('<str:city>/', forecast_view, name='forecast'),
]
