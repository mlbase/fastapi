from typing import Any
from typing_extensions import Self

from pydantic import BaseModel, Field, field_validator


class FriendBase(BaseModel):
    user_id: int = Field()
    friend_id: int = Field()

    # @field_validator('friend_id', 'user_id')
    # def validate(cls, value: Any):
    #     if cls.user_id == cls.friend_id:
    #         raise ValueError("자기 자신을 친구 추천할 수는 없습니다.")
    #     return


class FriendWithUser(FriendBase):
    username: str = Field()
    mutual_count: int = Field()