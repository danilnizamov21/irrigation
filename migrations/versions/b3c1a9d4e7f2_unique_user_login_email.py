"""unique user login and email

Revision ID: b3c1a9d4e7f2
Revises: 97ce2ed57e65
Create Date: 2026-09-12 23:55:00.000000

"""

from typing import Sequence, Union

from alembic import op

revision: str = "b3c1a9d4e7f2"
down_revision: Union[str, Sequence[str], None] = "97ce2ed57e65"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_user_login", "user", ["login"])
    op.create_unique_constraint("uq_user_email", "user", ["email"])


def downgrade() -> None:
    op.drop_constraint("uq_user_email", "user", type_="unique")
    op.drop_constraint("uq_user_login", "user", type_="unique")
