"""Remove Possession table

Revision ID: e0fecbd63211
Revises: ebfe30f426a9
Create Date: 2024-08-06 05:20:40.525042+09:00

"""
from alembic import op
import sqlalchemy as sa

revision = 'e0fecbd63211'
down_revision = 'ebfe30f426a9'
branch_labels = None
depends_on = None

def upgrade():
    # 外部キー制約を削除
    op.drop_constraint('possessions_friend_id_fkey', 'possessions', type_='foreignkey')
    op.drop_constraint('possessions_user_id_fkey', 'possessions', type_='foreignkey')

    # インデックスを削除
    op.drop_index('ix_possessions_friend_id', table_name='possessions')
    op.drop_index('ix_possessions_user_id', table_name='possessions')

    # テーブルを削除
    op.drop_table('possessions')

def downgrade():
    # テーブルを再作成
    op.create_table('possessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('friend_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # インデックスを再作成
    op.create_index('ix_possessions_user_id', 'possessions', ['user_id'], unique=False)
    op.create_index('ix_possessions_friend_id', 'possessions', ['friend_id'], unique=False)

    # 外部キー制約を再作成
    op.create_foreign_key('possessions_friend_id_fkey', 'possessions', 'friends', ['friend_id'], ['id'])
    op.create_foreign_key('possessions_user_id_fkey', 'possessions', 'users', ['user_id'], ['id'])
