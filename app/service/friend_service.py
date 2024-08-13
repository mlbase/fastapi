from typing import List

from pydantic import BaseModel


class RecommendListByMutualCount(BaseModel):
    mutual_count: int
    user_id: int
    full_name: str

class FriendService:
    def request_for_friend(self, ):
        pass

    def approve_for_friend(self, ):
        pass

    def find_mutual_friend_count(self, user_id: int, friend_id: int) -> int:
        assert user_id > 0 & friend_id > 0 & user_id != friend_id

    def find_recommend_list_by_mutual_count(self, user_id: int) -> List[RecommendListByMutualCount]:
        assert user_id > 0


friend_service = FriendService()
