from config import get_settings
from twilio.rest import Client


class SmsService:
    def __init__(self) -> None:
        settings = get_settings()
        self.twilio_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_from = settings.TWILIO_FROM
        self.client = Client(self.twilio_sid, self.twilio_token)

    async def send(self, text: str, to: str) -> None:
        if not to:
            raise RuntimeError("SMS recipient is missing")

        await self.client.messages.create_async(from_=self.twilio_from, to=to, body=text)
