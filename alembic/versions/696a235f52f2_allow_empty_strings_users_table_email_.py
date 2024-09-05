"""allow empty strings users table email & phone 2try

Revision ID: 696a235f52f2
Revises: b3aac8e6fc1b
Create Date: 2024-09-04 03:36:31.040453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '696a235f52f2'
down_revision: Union[str, None] = 'b3aac8e6fc1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
