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


@router.post("/{id}", response_model=int)
async def add_friend(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        id: int,
        current_user: model.User = Depends(dependencies.get_current_user)
) -> int:
    assert id > 0
    user_id = current_user.id
    friend_id = id
    await friend_service.add_friend(user_id, friend_id, db)
    return id


@router.delete("/{id}", response_model=None)
async def delete_friend(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        id: int,
        current_user: model.User = Depends(dependencies.get_current_user)
) -> Any:
    user_id = current_user.id
    friend_id = id
    await friend_service.delete_friend(user_id, friend_id, db)
    return


@router.get("/recommend")
async def get_recommend_list_by_mutual_count(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        current_user: model.User = Depends(dependencies.get_current_user),
) -> List[RecommendListByMutualCount]:
    user_id = current_user.id
    return await friend_service.find_recommend_list_by_mutual_count(user_id, db)


@router.get("/mutual/counts")
async def get_mutual_counts_with_someone(
        *,
        db: AsyncSession = Depends(dependencies.get_db),
        current_user: model.User = Depends(dependencies.get_current_user),
        checking_id: int = Query(example=113544, description="mutual_count 를 체크하려는 id")
) -> int:
    user_id = current_user.id
    return await friend_service.find_mutual_friend_count(user_id, checking_id, db)
