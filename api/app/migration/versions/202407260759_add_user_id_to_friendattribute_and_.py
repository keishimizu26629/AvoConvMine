"""Add user_id to FriendAttribute and create ConversationHistory table

Revision ID: p9uz3eb62fcg
Revises: ebc9e3ecbcdf
Create Date: 2024-07-26 08:10:10.848600+09:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'p9uz3eb62fcg'
down_revision = 'ebc9e3ecbcdf'  # 前のリビジョンIDを入力
branch_labels = None
depends_on = None


def upgrade():
    # FriendAttributeテーブルにuser_idカラムを追加
    op.add_column('friend_attributes', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_friend_attributes_user_id'), 'friend_attributes', ['user_id'], unique=False)
    op.create_foreign_key(None, 'friend_attributes', 'users', ['user_id'], ['id'])

    # ConversationHistoryテーブルを作成
    op.create_table('conversation_histories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('friend_id', sa.Integer(), nullable=False),
        sa.Column('conversation_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('context', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['friend_id'], ['friends.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversation_histories_friend_id'), 'conversation_histories', ['friend_id'], unique=False)
    op.create_index(op.f('ix_conversation_histories_user_id'), 'conversation_histories', ['user_id'], unique=False)


def downgrade():
    # ConversationHistoryテーブルを削除
    op.drop_index(op.f('ix_conversation_histories_user_id'), table_name='conversation_histories')
    op.drop_index(op.f('ix_conversation_histories_friend_id'), table_name='conversation_histories')
    op.drop_table('conversation_histories')

    # FriendAttributeテーブルからuser_idカラムを削除
    op.drop_constraint(None, 'friend_attributes', type_='foreignkey')
    op.drop_index(op.f('ix_friend_attributes_user_id'), table_name='friend_attributes')
    op.drop_column('friend_attributes', 'user_id')
