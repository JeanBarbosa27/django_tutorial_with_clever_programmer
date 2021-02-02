from django.urls import path

from .views import *

app_name = 'polls'

urlpatterns = [
    path('', index, name="index"),
]
