from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# local dependency
import crud
import model
import schema
from custom_exception.Exceptions import SQLException
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
