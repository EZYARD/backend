"""add-listings

Revision ID: 66d61b7d9162
Revises: 9017eb6eb0fd
Create Date: 2024-09-23 14:47:00.162748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66d61b7d9162'
down_revision: Union[str, None] = '9017eb6eb0fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
