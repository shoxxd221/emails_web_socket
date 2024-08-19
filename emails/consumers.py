import os

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import email
import json
from dotenv import load_dotenv

from .services import create_email
from .providers import GmailProvider, MailProvider, YandexProvider


load_dotenv()


class BaseMailConsumer(AsyncWebsocketConsumer):
    """Базовый consumer для почт"""
    def __init__(self, *args, **kwargs):
        """Инициализация полей"""
        super().__init__(*args, **kwargs)
        self.provider = None

    async def connect(self):
        """Подключение"""
        await self.accept()
        await sync_to_async(self.provider.login)()
        await sync_to_async(self.provider.get_inbox)()
        unseen_msg = await sync_to_async(self.provider.get_unseen_messages)()

        if unseen_msg:
            message_count = 1
            for letter in unseen_msg:
                res, msg = await sync_to_async(self.provider.get_message_by_uid)(letter)
                if res == 'OK':
                    email_obj = await sync_to_async(create_email)(email.message_from_bytes(msg[0][1]))
                    await self.send(json.dumps({
                        'message': f'{message_count} / {len(unseen_msg)}.',
                        'email_name': f'Тема: {email_obj.name}',
                        'email_text': f'Текст: {email_obj.text}',
                        'email_date': f'Дата получения: {email_obj.received_date}',
                    }))
                message_count += 1
            await sync_to_async(self.provider.mail.logout)()


class GmailConsumer(BaseMailConsumer):
    """Consumer для gmail.com"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = GmailProvider(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))


class MailConsumer(BaseMailConsumer):
    """Consumer для mail.ru"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = MailProvider(os.getenv('MAIL_USER'), os.getenv('MAIL_PASSWORD'))


class YandexConsumer(BaseMailConsumer):
    """Consumer для yandex.ru"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = YandexProvider(os.getenv('YANDEX_USER'), os.getenv('YANDEX_PASSWORD'))
