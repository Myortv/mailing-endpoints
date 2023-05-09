import re
from pydantic import BaseModel
from pydantic import validator


phonenumber_pattern = re.compile('^7[0-9]{10}$')
phonecode_pattern = re.compile('^[0-9]{3}$')


class ClientBase(BaseModel):
    phone_number: str
    mobile_operator_code: str
    tag: str
    timezone: str

    @validator('phone_number')
    def phone_number_correct(cls, v):
        if phonenumber_pattern.match(v):
            return v
        else:
            raise ValueError(f'phone number ({v}) is invalid')

    @validator('mobile_operator_code')
    def operator_code_correct(cls, v):
        if phonecode_pattern.match(v):
            return v
        else:
            raise ValueError(f'phone number ({v}) is invalid')

    # def cast_to_num(self):
    #     return

class ClientInDB(ClientBase):
    id: int

class ClientUpdate(ClientBase):
    pass
class ClientCreate(ClientBase):
    pass
