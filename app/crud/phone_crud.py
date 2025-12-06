from fastapi import HTTPException
from app.config import REDIS_CLIENT
from app.models.phone import Phone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.phone_schema import PhoneAddressResponse
import json


async def create_phone_address(phone: str, address: str, db: AsyncSession ):
    exists = await REDIS_CLIENT.exists(phone)

    if exists:
        raise HTTPException(status_code=409, detail="Phone already exists")
    phone = Phone(phone=phone, address=address)
    db.add(phone)
    await db.commit()
    await REDIS_CLIENT.set(phone.phone, json.dumps({"id": phone.id , "address": phone.address}))
    return phone


async def update_phone_address(phone: str, address: str, db: AsyncSession):
    exists = await REDIS_CLIENT.exists(phone)
    if not exists:
        raise HTTPException(status_code=404, detail="Phone not found")
    phone_obj = await phone_check(phone, db)
    phone_obj.address = address
    phone_obj.phone = phone    
    if phone != phone_obj.phone:
        await REDIS_CLIENT.delete(phone_obj.phone)
    await db.commit()
    await REDIS_CLIENT.set(phone_obj.phone, json.dumps({"id": phone_obj.id , "address": phone_obj.address}))
    return phone_obj


async def get_phone_address(phone: str):
    phone_data = await REDIS_CLIENT.get(phone)
    phone_data = json.loads(phone_data)
    if not phone_data:
        raise HTTPException(status_code=404, detail="Phone not found")
    return PhoneAddressResponse(phone=phone, address=phone_data["address"], id=phone_data["id"])


async def get_all_address(db: AsyncSession):
    all_address = await db.execute(select(Phone))
    return all_address.scalars().all()


async def delete_phone_address(phone: str, db: AsyncSession):
    exists = await REDIS_CLIENT.exists(phone)

    if not exists:
        raise HTTPException(status_code=404, detail="Phone not found")
   
    phone = await phone_check(phone, db)
    await db.delete(phone)
    await db.commit()
    await REDIS_CLIENT.delete(phone)
    return {"phone": phone}


async def phone_check(phone: str, db: AsyncSession):
    phone_check_query = await db.execute(select(Phone).where(Phone.phone == phone))
    phone_check =  phone_check_query.scalar_one_or_none()
    if not phone_check:
        raise HTTPException(status_code=404, detail="Phone not found")
    return phone_check