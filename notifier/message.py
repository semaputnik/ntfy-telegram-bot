import logging
from datetime import datetime
from typing import Optional

import pytz
from pydantic import BaseModel, field_validator


class Message(BaseModel):
    id: str
    time: datetime
    expires: Optional[datetime] = None
    event: str
    topic: str
    message: Optional[str] = None
    title: Optional[str] = None
    priority: Optional[int] = None
    tags: Optional[list[str]] = None

    @field_validator('time', mode='before')
    def parse_time(cls, value: int) -> datetime:
        dt = datetime.fromtimestamp(value)
        return dt.astimezone(pytz.timezone('Europe/Berlin'))

    @field_validator('expires', mode='before')
    def parse_expires(cls, value: Optional[int]) -> Optional[datetime]:
        if value is not None:
            dt = datetime.fromtimestamp(value)
            return dt.astimezone(pytz.timezone('Europe/Berlin'))
        else:
            return None


    def __repr__(self):
        return f"<Message(id={self.id}, time={self.time}, expires={self.expires}, event={self.event}, " \
               f"topic={self.topic}, message={self.message}, title={self.title}, priority={self.priority}, " \
               f"tags={self.tags})>"