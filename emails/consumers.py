import json
import os
from time import sleep
from dotenv import load_dotenv

from channels.generic.websocket import WebsocketConsumer

from .providers import *


load_dotenv()

gmail_provider = GmailProvider(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'), 'imap.gmail.com')
gmail_provider.login()
gmail_provider.get_inbox()


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        unseen_msg = gmail_provider.get_unseen_messages()

        if unseen_msg[0]:
            message_count = 1
            for letter in unseen_msg:
                res, msg = gmail_provider.get_message_by_uid(letter)
                if res == "OK":
                    email_obj = create_email(email.message_from_bytes(msg[0][1]))
                    self.send(json.dumps({
                        'message': f'{message_count} / {len(unseen_msg)}.',
                        'email': f'Тема: {email_obj.name}'
                    }))
                message_count += 1
                sleep(2)
            gmail_provider.mail.logout()
