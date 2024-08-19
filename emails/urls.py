from django.urls import path

from .views import gmail, mail


urlpatterns = [
    path('gmail', gmail),
    path('mail', mail),
]
