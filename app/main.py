import asyncio
from typing import List, Tuple

from mail import EmailService
from sms import SmsService
from telegram import TelegramService
from config import get_settings
from db import get_user


channels = {
    "email": EmailService(),
    "sms": SmsService(),
    "telegram": TelegramService(),
}


def _order_channels() -> List[str]:
    settings = get_settings()
    return [c for c in settings.CHANNEL_ORDER.split(",")]


async def send(user_id: int, text: str):
    user = get_user(user_id)
    if not user:
        print(f"User {user_id} not found")
        return

    settings = get_settings()
    order = _order_channels()

    for attempt in range(1, settings.MAX_RETRIES + 1):
        tried: List[Tuple[str, str]] = []

        for name in order:
            service = channels.get(name)
            if service is None:
                tried.append((name, "unavailable"))
                continue
            try:
                if name == "email":
                    service.send(text, to=user.email)
                elif name == "sms":
                    await service.send(text, to=user.phone)
                elif name == "telegram":
                    await service.send(text, to=user.telegram_id)
                else:
                    tried.append((name, "unknown_channel"))
                    continue
                print(f"Notification to user {user_id} sent via {name} (attempt {attempt})")
                return
            except Exception as exc:
                tried.append((name, f"error: {exc}"))
                continue

        if attempt < settings.MAX_RETRIES:
            print(f"All channels failed for user {user_id} on attempt {attempt}; retrying in {settings.RETRY_TIMEOUT}s")
            await asyncio.sleep(settings.RETRY_TIMEOUT)
        else:
            print(f"All channels failed for user {user_id} after {settings.MAX_RETRIES} attempts:")
            for name, reason in tried:
                print(f" - {name}: {reason}")
            return


if __name__ == "__main__":
    asyncio.run(send(1, 'Hello World'))
