from django.urls import path

from .consumers import GmailConsumer, MailConsumer, YandexConsumer


ws_urlpatterns = [
    path('ws/gmail/', GmailConsumer.as_asgi()),
    path('ws/mail/', MailConsumer.as_asgi()),
    path('ws/yandex/', YandexConsumer.as_asgi()),
]
