from fastapi import APIRouter, status
from app.schemas.phone_schema import PhoneAddressCreate, PhoneAddressResponse
from app.crud.phone_crud import (
    create_phone_address,
    update_phone_address,
    get_phone_address,
    get_all_address,
    delete_phone_address
)
from fastapi import Depends
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


router = APIRouter()

@router.post("/", response_model=PhoneAddressResponse, status_code=status.HTTP_201_CREATED)
async def create_phone(data: PhoneAddressCreate,  db: AsyncSession = Depends(get_db)):
    return await create_phone_address(data.phone, data.address, db)

@router.put("/{phone}", response_model=PhoneAddressResponse)
async def update_phone(phone: str, data: PhoneAddressCreate, db: AsyncSession = Depends(get_db)):
    return await update_phone_address(phone, data.address, db)


@router.get("/", response_model=List[PhoneAddressResponse])
async def get_all_phone(db: AsyncSession = Depends(get_db)):
    return await get_all_address(db)


@router.get("/{phone}", response_model=PhoneAddressResponse)
async def get_phone(phone: str):
    return await get_phone_address(phone)

@router.delete("/{phone}", response_model=dict)
async def delete_phone(phone: str, db: AsyncSession = Depends(get_db)):
    return await delete_phone_address(phone, db)
    