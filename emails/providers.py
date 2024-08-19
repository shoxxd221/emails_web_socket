from abc import ABC, abstractmethod
import imaplib


class ImportProvider(ABC):
    """Базовый класс провайдеров"""

    def __init__(self, user, password, imap_url):
        """Инициализация переменных"""
        self.user = user
        self.password = password
        self.imap_url = imap_url
        self.mail = imaplib.IMAP4_SSL(imap_url)

    @abstractmethod
    def get_inbox(self):
        """Метод для открытия папки входящие"""

    def get_message_by_uid(self, number) -> (str, list):
        """Получение сообщения по uid"""
        return self.mail.uid('fetch', number, '(RFC822)')

    def get_unseen_messages(self) -> list:
        """Получение непрочитанных сообщений"""
        res, unseen_msg = self.mail.uid('search', 'UNSEEN', 'ALL')
        unseen_msg = unseen_msg[0].decode('utf-8').split(' ')
        return unseen_msg

    def login(self):
        """Логин в почту"""
        self.mail.login(self.user, self.password)


class GmailProvider(ImportProvider):
    """Gmail провайдер"""

    def __init__(self, user, password):
        super().__init__(user, password, 'imap.gmail.com')

    def get_inbox(self):
        self.mail.select('inbox')


class MailProvider(ImportProvider):
    """Mail провайдер"""

    def __init__(self, user, password):
        super().__init__(user, password, 'imap.mail.ru')

    def get_inbox(self):
        self.mail.select('INBOX')
