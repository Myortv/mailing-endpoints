from typing import List, Optional

from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel

from app.schemas.client import ClientInDB

import asyncio


@dataclass
class Message:
    start_window: datetime
    end_window: datetime
    client_id: int
    phone: int
    timeout: Optional[datetime] = None


@dataclass
class Mailing:
    id: int
    start_at: datetime
    end_at: datetime
    body: str
    message_queue: List[Message] = field(default_factory=lambda: [])
    task: asyncio.Task | None = None
    timeout: datetime | None = None

    def set_message_queue(
        self,
        clients: List[ClientInDB],
    ):
        for client in clients:
            client_start = datetime.combine(datetime.now().date(), client.start_recieve)
            print('ggggggggggggggggggggggggggggggggggggggggggg')
            print(self.start_at)
            print(client_start)
            print('ggggggggggggggggggggggggggggggggggggggggggg')
            self.message_queue.append(Message(
                max(self.start_at, client_start),
                min(self.end_at, client_start + client.recieve_duration),
                client_id=client.id,
                phone=int(client.phone_number),
            ))

class MessageRequest(BaseModel):
    id: int
    phone: int
    text: str

class MessageResponse(BaseModel):
    code: int
    message: str
