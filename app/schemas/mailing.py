import datetime

from typing import Optional

from pydantic import BaseModel
from pydantic import validator


class MailingBase(BaseModel):
	start_time: Optional[datetime.datetime]
	end_time: datetime.datetime
	body: str
	filters: dict

	# @validator('start_time', 'end_time')
	# def is_time_valid(cls, v):
	# 	if v:
	# 		if v >= datetime.datetime.now():
	# 			return v
	# 		else:
	# 			raise ValueError(f'time ({v}) is too small!')



class MailingInDB(MailingBase):
	start_time: datetime.datetime
	id: int

class MailingUpdate(MailingBase):
	pass

