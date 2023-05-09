from dataclasses import dataclass
from datetime import datetime

from app.schemas.message import MessageInDB


@dataclass
class Message:
    message_object: MessageInDB
    start_window: datetime
    end_window: datetime
    timeout: datetime


@dataclass
class MessagePool:
    messages: List[Message] = []
