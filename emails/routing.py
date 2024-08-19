from django.urls import path

from .consumers import GmailConsumer, MailConsumer


ws_urlpatterns = [
    path('ws/gmail/', GmailConsumer.as_asgi()),
    path('ws/mail/', MailConsumer.as_asgi()),
]
