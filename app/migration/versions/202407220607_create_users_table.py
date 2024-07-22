"""create users table

Revision ID: 902391f922a1
Revises:
Create Date: 2024-07-22 06:07:44.031985+09:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '902391f922a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
    )

def downgrade():
    pass
    op.drop_table('users')
