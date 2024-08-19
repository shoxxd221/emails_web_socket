import base64
import email
import quopri
from datetime import datetime
from abc import ABC, abstractmethod
import imaplib
from email.header import decode_header
from bs4 import BeautifulSoup

from .models import Email


def create_email(msg):
    msg_date = date_parse(email.utils.parsedate_tz(msg["Date"]))
    msg_subj = from_subj_decode(msg["Subject"])
    letter_text = get_letter_text(msg)
    return Email.objects.create(name=msg_subj, received_date=msg_date, text=letter_text)


class ImportProvider(ABC):
    """Базовый класс провайдеров"""

    def __init__(self, user, password, imap_url):
        """Инициализация переменных"""
        self.user = user
        self.password = password
        self.imap_url = imap_url
        self.mail = imaplib.IMAP4_SSL(imap_url)

    def get_message_by_uid(self, number) -> (str, list):
        """Получение сообщения по uid"""
        return self.mail.uid("fetch", number, "(RFC822)")

    def get_unseen_messages(self) -> list:
        """Получение непрочитанных сообщений"""
        res, unseen_msg = self.mail.uid("search", "UNSEEN", "ALL")
        unseen_msg = unseen_msg[0].decode('utf-8').split(" ")
        return unseen_msg

    @abstractmethod
    def get_inbox(self):
        """Метод для открытия папки входящие"""

    def login(self):
        """Логин в почту"""
        self.mail.login(self.user, self.password)


def date_parse(msg_date):
    if not msg_date:
        return datetime.now()
    else:
        dt_obj = "".join(str(msg_date[:6]))
        dt_obj = dt_obj.strip("'(),")
        dt_obj = datetime.strptime(dt_obj, "%Y, %m, %d, %H, %M, %S")
        return dt_obj


def from_subj_decode(msg_from_subj):
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1]
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return None


def letter_type(part):
    if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:  # all possible types: quoted-printable, base64, 7bit, 8bit, and binary
        return part.get_payload()


def get_letter_text_from_html(body):
    body = body.replace("<div><div>", "<div>").replace("</div></div>", "</div>")
    try:
        soup = BeautifulSoup(body, "html.parser")
        paragraphs = soup.find_all("div")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text + "\n"
        return text.replace("\xa0", " ")
    except (Exception) as exp:
        print("text ftom html err ", exp)
        return False


def get_letter_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            count = 0
            if part.get_content_maintype() == "text" and count == 0:
                extract_part = letter_type(part)
                if part.get_content_subtype() == "html":
                    letter_text = get_letter_text_from_html(extract_part)
                else:
                    letter_text = extract_part.rstrip().lstrip()
                count += 1
                return (
                    letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")
                )
    else:
        count = 0
        if msg.get_content_maintype() == "text" and count == 0:
            extract_part = letter_type(msg)
            if msg.get_content_subtype() == "html":
                letter_text = get_letter_text_from_html(extract_part)
            else:
                letter_text = extract_part
            count += 1
            return letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")


class GmailProvider(ImportProvider):
    """Gmail провайдер"""

    def __init__(self, user, password, imap_url):
        super().__init__(user, password, imap_url)

    def get_inbox(self):
        self.mail.select('inbox')
