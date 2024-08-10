"""Create requests and responses tables

Revision ID: 5b8a5d022077
Revises: cc91657a37aa
Create Date: 2024-08-10 10:56:59.055956+09:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5b8a5d022077'
down_revision = 'cc91657a37aa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'requests',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, index=True),
        sa.Column('content', sa.Text),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )

    op.create_table(
        'responses',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('request_id', sa.Integer, sa.ForeignKey('requests.id'), unique=True),
        sa.Column('question_category', sa.Integer),
        sa.Column('who', sa.String, index=True),
        sa.Column('what', sa.String, index=True),
        sa.Column('related_subject', sa.String, nullable=True),
        sa.Column('status', sa.String),
        sa.Column('answer', sa.Text),
        sa.Column('approximation_attribute', sa.String),
        sa.Column('approximation_value', sa.String),
        sa.Column('similarity_category', sa.String),
        sa.Column('final_answer', sa.Text),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade():
    op.drop_table('responses')
    op.drop_table('requests')
