"""dummy-data

Revision ID: 60b3b68345ab
Revises: b7ca0e2dc793
Create Date: 2024-08-13 21:19:50.206480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from faker import Faker

# revision identifiers, used by Alembic.
revision: str = '60b3b68345ab'
down_revision: Union[str, None] = 'b7ca0e2dc793'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
faker = Faker()


def upgrade() -> None:
    conn = op.get_bind()

    # 유저 dummy data
    batch_size = 1000
    data = []
    for _ in range(100000):
        data.append({
            "full_name": faker.user_name(),
            "email": faker.email(),
            "hashed_password": faker.password()
        })
        if len(data) == batch_size:
            conn.execute(sa.text(
                """
                INSERT INTO api_user (full_name, email, hashed_password) VALUES (:full_name, :email, :hashed_password)
                ON CONFLICT(email) DO NOTHING
                """),
                data
            )
            data.clear()

    if data:
        conn.execute(sa.text(
            """
            INSERT INTO api_user (full_name, email, hashed_password) VALUES (:full_name, :email, :hashed_password)
            ON CONFLICT(email) DO NOTHING
            """),
            data
        )

    # 친구관계 dummy data
    user_ids = conn.execute(sa.text("SELECT id FROM api_user")).fetchall()
    user_ids = {row[0] for row in user_ids}
    user_pairs= []
    for _ in range(10000):
        user_id = faker.random_element(list(user_ids))
        friend_id = faker.random_element(list(user_ids))

        if user_id in user_ids and friend_id in user_ids and user_id != friend_id:
            user_pairs.append({"user_id": user_id, "friend_id": friend_id, "is_delete": False})
    print(user_pairs[:10])  # Print the first 10 entries to verify

    conn.execute(sa.text(
        """
        INSERT INTO friendship(user_id, friend_id, is_delete) VALUES(:user_id, :friend_id, :is_delete)
        ON CONFLICT(user_id, friend_id) DO NOTHING; 
        """
    ), user_pairs
    )
    conn.commit()


def downgrade() -> None:
    truncate_query = ("TRUNCATE TABLE api_user;"
                      "TRUNCATE TABLE friendship;")
    conn = op.get_bind()
    conn.execute(sa.text(truncate_query))
