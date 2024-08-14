from typing import Any, Dict, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.base import CRUDBase
from model.friendship import friendship
from schema.friendship import FriendBase, FriendWithUser
from crud.crud_user import user
from custom_exception.Exceptions import SQLException


class CRUDFriend(CRUDBase[friendship, FriendBase, FriendWithUser]):

    async def create(self, session: AsyncSession, obj_in: FriendBase) -> Any:
        if not user.get(session, obj_in.user_id):
            raise SQLException
        if not user.get(session, obj_in.friend_id):
            raise SQLException
        db_obj = friendship(
            obj_in.user_id,
            obj_in.friend_id
        )

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

    async def delete(self, session: AsyncSession, *, obj_in: FriendBase) -> Any:
        is_delete = True
        if not user.get(session, obj_in.user_id):
            raise SQLException
        if not user.get(session, obj_in.friend_id):
            raise SQLException
        db_obj = friendship(
            obj_in.user_id,
            obj_in.friend_id,
            is_delete
        )

        await session.commit()


friend = CRUDBase(friendship)
