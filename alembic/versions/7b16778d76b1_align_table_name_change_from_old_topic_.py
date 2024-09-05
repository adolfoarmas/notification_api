"""Align table name change from old_topic_name to new_category_name

Revision ID: 7b16778d76b1
Revises: d6f4b9b11a6a
Create Date: 2024-09-04 01:01:51.329795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b16778d76b1'
down_revision: Union[str, None] = 'd6f4b9b11a6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
