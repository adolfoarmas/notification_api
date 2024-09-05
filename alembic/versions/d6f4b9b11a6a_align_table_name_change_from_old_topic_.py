"""Align table name change from old_topic_name to new_category_name

Revision ID: d6f4b9b11a6a
Revises: 22ddcaa8e0ac
Create Date: 2024-09-04 00:56:44.502900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6f4b9b11a6a'
down_revision: Union[str, None] = '22ddcaa8e0ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
