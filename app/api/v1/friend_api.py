from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

# local dependency
import crud
import model
import schema
from custom_exception.Exceptions import SQLException
from service import RecommendListByMutualCount
from service.friend_service import friend_service
from utils import dependencies

router = APIRouter()


@router.post("/", response_model=schema.friendship.FriendBase)
async def add_friend(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        item_in: schema.friendship.FriendBase,
        current_user: model.user = Depends(dependencies.get_current_user),
) -> Any:
    item = await crud.friend.create(db, item_in)
    return item


@router.delete("/{id}", response_model=schema.friendship.FriendBase)
async def delete_friend(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        id: int,
        current_user: model.User = Depends(dependencies.get_current_user)
) -> Any:
    q_object = await crud.friend.remove(db=db, id=id)
    item = q_object
    print(item)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.friend.remove(db=db, id=id)

    return item


@router.get("/recommend")
async def get_recommend_list_by_mutual_count(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        user_id: int = Query(example=180697, description="현재 id 추후 jwt 토큰으로 제거 예정"),
) -> List[RecommendListByMutualCount]:
    return await friend_service.find_recommend_list_by_mutual_count(user_id, db)


@router.get("/mutual/counts")
async def get_mutual_counts_with_someone(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        user_id: int = Query(example=180697, description="현재 id 추후 jwt 토큰으로 제거 예정"),
        checking_id: int = Query(example=113544, description="mutual_count 를 체크하려는 id")
) -> int:
    return await friend_service.find_mutual_friend_count(user_id, checking_id, db)
