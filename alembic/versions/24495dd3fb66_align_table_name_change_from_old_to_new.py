"""Align table name change from old  to new

Revision ID: 24495dd3fb66
Revises: 7a1cc1c75432
Create Date: 2024-09-04 01:08:29.677044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24495dd3fb66'
down_revision: Union[str, None] = '7a1cc1c75432'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user_topics', 'topic_id', new_column_name='category_id')
    
    op.rename_table('topics', 'categories')
    op.rename_table('user_topics', 'user_categories')

def downgrade() -> None:
    pass
