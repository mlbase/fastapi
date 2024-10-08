# pip dependency
from typing import Any

from sqlalchemy import Result, CursorResult, text, TextClause
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWSSignatureError
from pydantic import ValidationError
from jinja2 import Template
# local dependency
import model
from config.session_factory import engine, SQLALCHEMY_DATABASE_URL
from model import User
from schema.token import Token, TokenPayload
from config import security
from config.setting import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/logins/access_token")
sql_directory = 'sqls'


async def get_db() -> AsyncSession:
    db = AsyncSession(bind=engine)
    try:
        yield db
    finally:
        await db.close()


async def get_current_user(
        token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
) -> Result[tuple[User]]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    except JWSSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유효한 jwt가 아닙니다."
        )
    id: int = token_data.sub
    query = select(model.User).where(model.User.id == id)
    print(query)
    try:
        result = await session.execute(query)
        user = result.scalar_one_or_none()
    except SQLAlchemyError:
        raise SQLAlchemyError
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def render_sql_templates(template_name: str) -> text:
    with open(sql_directory + "/" + template_name + ".sql") as file:
        template = Template(file.read())
    return text(template.render())
