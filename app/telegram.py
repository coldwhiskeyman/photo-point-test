from aiogram import Bot
from config import get_settings


class TelegramService:
    def __init__(self) -> None:
        settings = get_settings()
        self.bot_token = settings.TG_BOT_TOKEN
        self.bot = Bot(token=self.bot_token)

    async def send(self, text: str, to: int) -> None:
        if not to:
            raise RuntimeError("Telegram chat_id is missing")

        await self.bot.send_message(chat_id=to, text=text)
