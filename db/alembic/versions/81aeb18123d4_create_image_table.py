"""Create image table

Revision ID: 81aeb18123d4
Revises: 9017eb6eb0fd
Create Date: 2024-10-07 11:25:44.396063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '81aeb18123d4'
down_revision: Union[str, None] = '9017eb6eb0fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'image',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('listing_id', sa.Integer, nullable=False),
        sa.Column('image_data', sa.LargeBinary, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('image')
