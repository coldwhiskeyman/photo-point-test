import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from db import create_user, get_user
from main import send


app = FastAPI()


class UserCreateRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    telegram_id: Optional[int] = None


class UserResponse(UserCreateRequest):
    id: int


class NotificationRequest(BaseModel):
    user_id: int
    text: str


class NotificationResponse(BaseModel):
    message: str


@app.post("/users/add", response_model=UserResponse)
async def create_user(user_data: UserCreateRequest):
    user = create_user(
        email=user_data.email,
        phone=user_data.phone,
        telegram_id=user_data.telegram_id
    )
    return UserResponse(
        id=user.id,
        email=user.email,
        phone=user.phone,
        telegram_id=user.telegram_id
    )


@app.post("/notification", response_model=NotificationResponse)
async def send_notification(notification: NotificationRequest):
    user = get_user(notification.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {notification.user_id} not found")

    asyncio.create_task(send(notification.user_id, notification.text))
    
    return NotificationResponse(
        message=f"Notification has sent to user {notification.user_id}"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
