import json
import os
from dotenv import load_dotenv
import email

from channels.generic.websocket import WebsocketConsumer

from .providers import GmailProvider, MailProvider
from .services import create_email


load_dotenv()


class GmailConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        gmail_provider = GmailProvider(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))
        gmail_provider.login()
        gmail_provider.get_inbox()
        unseen_msg = gmail_provider.get_unseen_messages()

        if unseen_msg[0]:
            message_count = 1
            for letter in unseen_msg:
                res, msg = gmail_provider.get_message_by_uid(letter)
                if res == 'OK':
                    email_obj = create_email(email.message_from_bytes(msg[0][1]))
                    self.send(json.dumps({
                        'message': f'{message_count} / {len(unseen_msg)}.',
                        'email_name': f'Тема: {email_obj.name}',
                        'email_text': f'Текст: {email_obj.text}',
                        'email_date': f'Дата получения: {email_obj.received_date}',
                    }))
                message_count += 1
            gmail_provider.mail.logout()


class MailConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        mail_provider = MailProvider(os.getenv('MAIL_USER'), os.getenv('MAIL_PASSWORD'))
        mail_provider.login()
        mail_provider.get_inbox()
        unseen_msg = mail_provider.get_unseen_messages()

        if unseen_msg[0]:
            message_count = 1
            for letter in unseen_msg:
                res, msg = mail_provider.get_message_by_uid(letter)
                if res == 'OK':
                    email_obj = create_email(email.message_from_bytes(msg[0][1]))
                    self.send(json.dumps({
                        'message': f'{message_count} / {len(unseen_msg)}.',
                        'email_name': f'Тема: {email_obj.name}',
                        'email_text': f'Текст: {email_obj.text}',
                        'email_date': f'Дата получения: {email_obj.received_date}',
                    }))
                message_count += 1
            mail_provider.mail.logout()
