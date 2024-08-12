from typing import Any, Dict, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import model
from config.security import get_password_hash, verify_password
from crud.base import CRUDBase
from model.user import User
from schema.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, session: AsyncSession, *, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        q_object = await session.execute(statement=statement, params={"email_1": email})
        return q_object.scalars().first()

    async def create(self, session: AsyncSession, *, obj_in: UserCreate) -> Any:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name
        )

        session.add(db_obj)
        await session.commit()

    async def update(self, session: AsyncSession, *, obj_in: Union[UserUpdate, Dict[str, Any]], **kwargs) -> Any:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        await super().update(session, db_obj=user, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        print(user)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return await user

    async def is_active(self, user: User) -> bool:
        return await user.is_active

    async def get_by_id(self, session: AsyncSession, id: int) -> None:
        statement = select(model.User).options(selectinload(model.User.items)) \
            .filter(model.User.id == id)

        q_object = await session.execute(statement=statement)
        result = q_object.scalar()
        return result

    async def get_by_id_raw(self, session: AsyncSession, id: int) -> User | None:
        user = await self.get(session, id)
        return user


user = CRUDUser(User)
