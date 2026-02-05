from pydantic import BaseModel


class Message(BaseModel):
    sender_id: str
    room_id: str
    content: str