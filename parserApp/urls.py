from django.urls import path, include
from .views import home, check


urlpatterns = [
    path('', home),
    path('check', check),
]
