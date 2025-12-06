from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

from app.models.user import User  # Import the User model
from app.schemas.auth_schema import UserResponse # Import the UserResponse schema



async def personal_get_user_data(db: AsyncSession, user_id: int) -> UserResponse:
    result = await db.execute(
        select(User)
        .filter(User.id == user_id)
        )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(
                    id=user.id,
                    username=user.username,
                    is_admin=user.is_admin,
                    is_active=user.is_active,
                    
                    )
