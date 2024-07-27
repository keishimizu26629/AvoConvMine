"""Remove embedding from Attribute and add to FriendAttribute

Revision ID: 2ce23d9a7ba7
Revises: p9uz3eb62fcg
Create Date: 2024-07-27 07:42:38.580474+09:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2ce23d9a7ba7'
down_revision = 'p9uz3eb62fcg'
branch_labels = None
depends_on = None


def upgrade():
    # Remove embedding column from Attribute table
    op.drop_column('attributes', 'embedding')

    # Add embedding column to FriendAttribute table
    op.add_column('friend_attributes', sa.Column('embedding', sa.Text(), nullable=True))

def downgrade():
    # Remove embedding column from FriendAttribute table
    op.drop_column('friend_attributes', 'embedding')

    # Add embedding column back to Attribute table
    op.add_column('attributes', sa.Column('embedding', sa.Text(), nullable=True))
