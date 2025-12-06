#!/usr/bin/env python3
"""
CLI-скрипт для создания администратора
"""

import asyncio
import sys
from app.db import AsyncSessionLocal
from sqlalchemy import select
from app.models.user import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Хэширование пароля"""
    return pwd_context.hash(password)

# Создание администратора
async def create_admin_user(
    username: str,
    password: str
):
    """
    Создание администратора
    
    Args:
        username: Имя пользователя
        password: Пароль
        first_name: Имя
        last_name: Фамилия
    
    Returns:
        User: Созданный администратор
    """
    async with AsyncSessionLocal() as session:
        # Проверка существования пользователя
        result = await session.execute(
            select(User).where(User.username == username)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise ValueError(f"Пользователь {username} уже существует")
        
        # Создание нового администратора
        admin_user = User(
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True,
           is_admin=True
        )
        
        session.add(admin_user)
        await session.commit()
        await session.refresh(admin_user)
        
        return admin_user


async def main():
    """Основная функция"""
    print("=== Создание администратора ===")
    print()
    
    # Получение данных пользователя
    username = input("Имя пользователя: ").strip()
    if not username:
        print("Ошибка: имя пользователя не может быть пустым")
        return
    
    password = input("Пароль: ").strip()
    if not password:
        print("Ошибка: пароль не может быть пустым")
        return
    
    confirm_password = input("Подтвердите пароль: ").strip()
    if password != confirm_password:
        print("Ошибка: пароли не совпадают")
        return
    

    print()
    print("Создание администратора...")
    
    try:
        # Создание администратора
        admin_user = await create_admin_user(
            username=username,
            password=password
        )
        
        print("✅ Администратор успешно создан!")
        print(f"Имя пользователя: {admin_user.username}")
 

    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
