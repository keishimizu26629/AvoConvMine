"""Add hashed_password to User model

Revision ID: cc91657a37aa
Revises: d5cca72da3ca
Create Date: 2024-08-08 00:35:43.847952+09:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cc91657a37aa'
down_revision = 'd5cca72da3ca'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('hashed_password', sa.String(length=128), nullable=True))


def downgrade():
    op.drop_column('users', 'hashed_password')
