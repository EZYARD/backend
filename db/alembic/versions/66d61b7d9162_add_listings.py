"""add-listings

Revision ID: 66d61b7d9162
Revises: 9017eb6eb0fd
Create Date: 2024-09-23 14:47:00.162748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '66d61b7d9162'
down_revision: Union[str, None] = '81aeb18123d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('listings',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),

                    sa.Column('name', sa.String(), nullable=False),

                    #address information is broken up into these 5 variables
                    sa.Column('streetNumber', sa.String(), nullable=False),
                    sa.Column('streetName', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('zipcode', sa.Integer(), autoincrement=False, nullable=False),

                    sa.Column('description', sa.String(), nullable=False),

                    sa.Column('startTime', sa.DateTime(), autoincrement=False, nullable=False),

                    sa.Column('endTime', sa.DateTime(), autoincrement=False, nullable=False),

                    #storade as a comma separated list
                    sa.Column('tags', sa.String(), nullable=True),

                    #this version of both price range and rating is based on the assumption that we will be using
                    #a simplified 1-5 dollar sign rating or 1-5 star rating system
                    sa.Column('priceRange', sa.Integer(), nullable=True),

                    sa.Column('rating', sa.Integer(), nullable=True),

                    #this version of reviews allows for one singular review, will look into how store multiple per
                    #column, likely some kinda of array of strings
                    sa.Column('reviews', sa.String(), nullable=True),


                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('listings')