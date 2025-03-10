from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from app.adapters.api.schemas.pagination import PaginatedResponse
from app.infrastructure.database.models.user import User
from app.adapters.api.schemas.user import UserCreate
from app.adapters.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.user_repository = UserRepository(db)

    async def create_user(self, user_create: UserCreate) -> User :
        user = await self.user_repository.create_user(user_create)
        return user

    async def get_users(self, offset: int, limit: int) -> PaginatedResponse:
        return await self.user_repository.get_users(offset, limit)
    
    async def get_user_by_id(self, id: int) -> User:
        user = await self.user_repository.get_user_by_id(id)
        if user:
            return user
        else:
            raise status.HTTP_404_NOT_FOUND

    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_repository.get_user_by_email(email)
        return user
