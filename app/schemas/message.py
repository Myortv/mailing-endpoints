import datetime

from typing import Optional

from pydantic import BaseModel
from pydantic import validator

phonenumber_pattern = re.compile('^7[0-9]{10}$')

class MessageBase(BaseModel):
	creation_time: Optional[datetime.datetime]
	mailing_id: int
	client_id: int
	status: Optional[str]

	@validator('mailing_id', 'client_id')
	def is_positive(cls, v):
		if v > 0:
			return v
		else:
			raise ValueError(
				f'Foreign key value ({v}) should be positive int'
			)

	# @validator('start_time', 'end_time')
	# def is_time_valid(cls, v):
	# 	if v:
	# 		if v >= datetime.datetime.now():
	# 			return v
	# 		else:
	# 			raise ValueError(f'time ({v}) is too small!')


class MessageInDB(MessageBase):
	status: str
	creation_time: datetime.datetime
	id: int

class MessageOutPut(BaseModel):
	id: int
	phone: str
	text: str

    @validator('phone')
    def phone_number_correct(cls, v):
        if phonenumber_pattern.match(v):
            return v
        else:
            raise ValueError(f'phone number ({v}) is invalid')

# class MessageUpdate(MessageBase):
# 	pass

