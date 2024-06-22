from pydantic import BaseModel
from typing import Optional
from datetime import date

# Model do przesyłania danych kontaktu przy tworzeniu
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    extra_data: Optional[str] = None

# Model do przesyłania danych kontaktu z ID
class Contact(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True