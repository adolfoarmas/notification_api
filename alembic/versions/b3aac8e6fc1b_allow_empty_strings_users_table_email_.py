"""allow empty strings users table email & phone 

Revision ID: b3aac8e6fc1b
Revises: 24495dd3fb66
Create Date: 2024-09-04 03:31:09.122593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3aac8e6fc1b'
down_revision: Union[str, None] = '24495dd3fb66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
