from pydantic import BaseModel

class PhoneAddressCreate(BaseModel):
    phone: str
    address: str

class PhoneAddressResponse(PhoneAddressCreate):
    id: int

    class Config:
        orm_mode = True