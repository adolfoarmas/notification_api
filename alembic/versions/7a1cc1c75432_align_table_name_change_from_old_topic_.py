"""Align table name change from old_topic_name to new_category_name

Revision ID: 7a1cc1c75432
Revises: 7b16778d76b1
Create Date: 2024-09-04 01:05:57.157259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a1cc1c75432'
down_revision: Union[str, None] = '7b16778d76b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
