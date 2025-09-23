import smtplib
from email.message import EmailMessage

from config import get_settings


class EmailService:
    def __init__(self) -> None:
        settings = get_settings()
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_use_tls = settings.SMTP_USE_TLS
        self.sender = settings.EMAIL_FROM
        self.server = smtplib.SMTP(self.smtp_host, self.smtp_port)


    def send(self, text: str, to: str) -> None:
        if not to:
            raise RuntimeError("Email recipient is missing")

        msg = EmailMessage()
        msg["From"] = self.sender
        msg["To"] = to
        msg["Subject"] = "Notification"
        msg.set_content(text)

        if self.smtp_use_tls:
            self.server.starttls()
        self.server.ehlo()
        self.server.login(self.smtp_user, self.smtp_password)
        self.server.send_message(msg)
        self.server.quit()


