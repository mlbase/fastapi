from typing import Set

from sqlalchemy import Boolean, Column, Integer, String, and_
from sqlalchemy.orm import relationship, Mapped, foreign

from config.base_class import ORMBase
from model.friendship import friendship


class User(ORMBase):
    __tablename__ = "api_user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    friends: Mapped[Set["User"]] = relationship(
        'User',
        secondary=friendship,
        primaryjoin=and_(
            id == foreign(friendship.c.user_id),
            friendship.c.is_delete == False
        ),
        secondaryjoin=id == foreign(friendship.c.friend_id),
        back_populates='friend_of'
    )
    friend_of: Mapped[Set["User"]] = relationship(
        'User',
        secondary=friendship,
        primaryjoin=and_(
            id == foreign(friendship.c.friend_id),
            friendship.c.is_delete == False
        ),
        secondaryjoin=id == foreign(friendship.c.user_id),
        back_populates='friends'
    )
