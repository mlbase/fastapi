from typing import List

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.future import select
from sqlalchemy import update

import model
from utils.dependencies import render_sql_templates
from custom_exception.Exceptions import UserNotFoundException


class RecommendListByMutualCount(BaseModel):
    mutual_count: int
    user_id: int
    full_name: str

    class config:
        orm_mode = True


class FriendService:
    def request_for_friend(self, ):
        pass

    def approve_for_friend(self, ):
        pass

    async def add_friend(self, user_id: int, friend_id: int, db: AsyncSession):
        assert 0 < user_id != friend_id > 0
        result = await db.execute(select(model.User).where(model.User.id == friend_id))
        friend = result.scalar_one_or_none()
        if not friend:
            raise UserNotFoundException
        stmt = upsert(model.friendship).values(
            user_id=user_id, friend_id=friend_id, is_delete=False
        ).on_conflict_do_update(
            index_elements=['user_id', 'friend_id'],
            set_={"is_delete": False}
        )
        stmt_reverse = upsert(model.friendship).values(
            user_id=friend_id, friend_id=user_id, is_delete=False
        ).on_conflict_do_update(
            index_elements=['user_id', 'friend_id'],
            set_={"is_delete": False}
        )
        await db.execute(stmt)
        await db.execute(stmt_reverse)
        await db.commit()

    async def delete_friend(self, user_id: int, friend_id: int, db: AsyncSession):
        assert 0 < user_id != friend_id > 0
        result = await db.execute(select(model.User).where(model.User.id == friend_id))
        friend = result.scalar_one_or_none()
        if not friend:
            raise UserNotFoundException
        friendship = model.friendship
        stmt = (update(friendship).
                where(friendship.c.user_id == user_id, friendship.c.friend_id == friend_id).
                values(is_delete=True))
        stmt_reverse = (update(friendship).
                        where(friendship.c.user_id == friend_id, friendship.c.friend_id == user_id).
                        values(is_delete=True))
        await db.execute(stmt)
        await db.execute(stmt_reverse)
        await db.commit()

    async def find_mutual_friend_count(self, user_id: int, checking_id: int, db: AsyncSession) -> int:
        assert 0 < user_id != checking_id > 0
        statement = render_sql_templates("get_mutual_friend_count")
        result = await db.execute(statement, {"user_id": user_id, "checking_id": checking_id})
        return result.scalar()

    async def find_recommend_list_by_mutual_count(self, user_id: int, db: AsyncSession) -> List[
        RecommendListByMutualCount]:
        assert user_id > 0
        statement = render_sql_templates("get_user_and_mutual_count_list")
        result = await db.execute(statement, {"user_id": user_id})
        processing_list = result.fetchall()
        return [RecommendListByMutualCount(mutual_count=row[0], user_id=row[1], full_name=row[2]) for row in
                processing_list]


friend_service = FriendService()
