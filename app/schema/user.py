from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Set


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(example="email id@domain.com")
    is_active: Optional[bool] = Field(example="사용 여부")
    full_name: Optional[str] = Field(example="사용 이름")

    class Config:
        json_schema_extra = {
            "email": "user@example.com",
            "is_active": True,
            "full_name": "example name",
            "items": [
                {
                    "title": "item title",
                    "description": "this item is..."
                }
            ]
        }


class UserCreate(UserBase):
    email: EmailStr = Field(example="id@domain.com")
    password: str = Field(example="비밀번호")


class UserUpdate(UserBase):
    password: Optional[str] = Field(example="비밀번호")


class UserInDBBase(UserBase):
    id: int | None = Field("db index")

    class Config:
        from_attributes = True


class User(UserInDBBase):
    friends: Set[UserBase]

    class Config:
        orm_mode = True



class UserInDB(UserInDBBase):
    hashed_password: str


class UserWithFriends(UserBase):
    friend_list: List[UserBase]



