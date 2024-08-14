from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Body, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic import Field
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

#######################
import crud
import model
import schema
from config.security import get_password_hash
from config.session_factory import SQLALCHEMY_DATABASE_URL
from utils.dependencies import get_db, get_current_user
from schema.user import UserWithFriends

router = APIRouter()


class UpdateUser(BaseModel):
    email: EmailStr = Field(description="요청할 이메일")
    password: str = Field(description="변경할 비밀번호")
    full_name: str = Field(description="변경할 이름")


@router.get("/", response_model=List[schema.User])
def read_users(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """

    :param db: orm_session
    :param skip: offset
    :param limit: rows per page
    :return:
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users
    # return ''


@router.post(
    "/", response_model=schema.User
)
async def create_user(
        *,
        db: AsyncSession = Depends(get_db),
        user_in: schema.UserCreate,
) -> Any:
    """
    # testestset

    - test!00

    """

    result = await crud.user.get_by_email(db, email=user_in.email)
    # while not result.raw.closed:
    #     await anyio.sleep(delay=0.1)
    user = result
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    await crud.user.create(db, obj_in=user_in)
    return Response(status_code=201, content=user_in.model_dump_json())


@router.patch("/me", response_model=schema.User)
async def update_user_me(
        *,
        request: UpdateUser,
        db: AsyncSession = Depends(get_db),
        current_user: model.User = Depends(get_current_user)
) -> Any:
    """

    user update 하는 api \n
    bearer-token needed
    """

    user_in = request
    if request.password is not None:
        user_in.password = get_password_hash(password=request.password)
    if request.full_name is not None:
        user_in.full_name = request.full_name
    if request.email is not None:
        user_in.email = request.email
    value_map = dict(email=user_in.email, full_name=user_in.full_name, password=user_in.password)
    await crud.user.update(db, obj_in=value_map)

    return Response(status_code=200, content=current_user)
    # return user_in


@router.get("/me", response_model=schema.User)
def read_user_me(
        db: AsyncSession = Depends(get_db),
        current_user: model.User = Depends(get_current_user)
) -> Any:
    """

    :param db: orm_session
    :param current_user: current user
    :return: User | None
    """
    return current_user


@router.get("/open", response_model=schema.User)
def create_user_open(
        *,
        db: AsyncSession = Depends(get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(None)
) -> Any:
    """

    :param db: orm_session
    :param password: input
    :param email: input
    :param full_name: input
    :return: User | None
    """
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="the user with this username already exist in the system"
        )
    user_in = schema.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.patch("/{user_id}", response_model=schema.User)
def update_user(
        *,
        db: AsyncSession = Depends(get_db),
        user_id: int,
        user_in: schema.UserUpdate = Body(
            example={
                "email": "test@example.com",
                "password": "test",
                "full_name": "testing..."
            }
        ),
) -> Any:
    """

    :param db: orm_session
    :param user_id: input via path_variable
    :param user_in: updating dto
    :return:
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="the user with this username does not exist in the system",
        )
    user = crud.user.update(db, obj_in=user_in)
    return user
