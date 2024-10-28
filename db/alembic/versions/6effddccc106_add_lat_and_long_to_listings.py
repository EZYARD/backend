"""add lat and long to listings

Revision ID: 6effddccc106
Revises: 66d61b7d9162
Create Date: 2024-10-27 22:28:00.879748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6effddccc106'
down_revision: Union[str, None] = '66d61b7d9162'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('listings', sa.Column('latitude', sa.Float, nullable=True))
    op.add_column('listings', sa.Column('longitude', sa.Float, nullable=True))


def downgrade() -> None:
    op.drop_column('listings', 'latitude')
    op.drop_column('listings', 'longitude')
