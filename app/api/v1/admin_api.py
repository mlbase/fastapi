from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from config.session_factory import SQLALCHEMY_DATABASE_URL

router = APIRouter()


@router.get("/")
async def admin_testing() -> Any:
    return {"detail": "Hello This is AdminPage"}