"""Add enabled column to friend_attributes

Revision ID: d5cca72da3ca
Revises: e0fecbd63211
Create Date: 2024-08-06 05:34:06.209871+09:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5cca72da3ca'
down_revision = 'e0fecbd63211'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('friend_attributes', sa.Column('enabled', sa.Boolean(), nullable=False, server_default='true'))

def downgrade():
    op.drop_column('friend_attributes', 'enabled')
