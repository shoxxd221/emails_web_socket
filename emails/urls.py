from django.urls import path

from .views import gmail, mail, yandex


urlpatterns = [
    path('gmail', gmail),
    path('mail', mail),
    path('yandex', yandex)
]
