import bcrypt
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegisterRequest


def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def register(self, data: UserRegisterRequest) -> User:
        if await self._repository.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        if await self._repository.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )
        return await self._repository.create(
            email=data.email,
            username=data.username,
            hashed_password=_hash_password(data.password),
        )
