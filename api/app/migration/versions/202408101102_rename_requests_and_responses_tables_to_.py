"""Rename requests and responses tables to chat_requests and chat_responses

Revision ID: 85154f2053fa
Revises: 5b8a5d022077
Create Date: 2024-08-10 11:02:58.000336+09:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '85154f2053fa'
down_revision = '5b8a5d022077'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('requests', 'chat_requests')
    op.rename_table('responses', 'chat_responses')


def downgrade():
    op.rename_table('chat_requests', 'requests')
    op.rename_table('chat_responses', 'responses')
