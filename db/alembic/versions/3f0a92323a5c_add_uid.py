"""add uid

Revision ID: 3f0a92323a5c
Revises: 6effddccc106
Create Date: 2024-11-03 22:14:14.161830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f0a92323a5c'
down_revision: Union[str, None] = '6effddccc106'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('listings', sa.Column('uid', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('listings', 'uid')
