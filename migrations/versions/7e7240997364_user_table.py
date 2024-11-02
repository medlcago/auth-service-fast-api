"""user table

Revision ID: 7e7240997364
Revises: 
Create Date: 2024-10-30 09:19:25.750825

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7e7240997364'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=32), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('password', sa.String(length=100), nullable=False),
                    sa.Column('is_active', sa.Boolean(), server_default='0', nullable=False),
                    sa.Column('is_admin', sa.Boolean(), server_default='0', nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
                    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
                    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
                    )


def downgrade() -> None:
    op.drop_table('users')
