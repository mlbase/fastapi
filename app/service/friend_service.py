from typing import List

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from utils.dependencies import render_sql_templates


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
        return [RecommendListByMutualCount(mutual_count=row[0], user_id=row[1], full_name=row[2]) for row in processing_list]


friend_service = FriendService()
