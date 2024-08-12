from config.base_class import ORMBase
from sqlalchemy import Table, Column, ForeignKey, Boolean, Integer

friendship = Table(
    "friendship",
    ORMBase.metadata,
    Column("user_id", Integer, ForeignKey("api_user.id"), primary_key=True),
    Column("friend_id", Integer,ForeignKey("api_user.id"), primary_key=True),
    Column("is_delete", Boolean(), default=False)
)

