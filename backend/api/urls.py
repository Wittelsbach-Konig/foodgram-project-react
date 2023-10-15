from django.urls import include, path
from rest_framework import routers

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]
