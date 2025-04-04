"""Update users table structure

Revision ID: ebc9e3ecbcdf
Revises: ab9a9b716f18
Create Date: 2024-07-25 06:56:09.848600+09:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ebc9e3ecbcdf'
down_revision = 'ab9a9b716f18'
branch_labels = None
depends_on = None


def upgrade():
    # users テーブルはすでに存在するため、新しいカラムのみを追加
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    op.add_column('users', sa.Column('firebase_uid', sa.String(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_firebase_uid'), 'users', ['firebase_uid'], unique=True)

    # friends テーブルが存在しない場合のみ作成
    if not op.has_table('friends'):
        op.create_table('friends',
            sa.Column('id', sa.INTEGER(), nullable=False),
            sa.Column('user_id', sa.INTEGER(), nullable=True),
            sa.Column('name', sa.VARCHAR(), nullable=True),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
            sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='friends_user_id_fkey'),
            sa.PrimaryKeyConstraint('id', name='friends_pkey')
        )
        op.create_index('ix_friends_name', 'friends', ['name'], unique=False)
        op.create_index('ix_friends_id', 'friends', ['id'], unique=False)

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friends',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('friends_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='friends_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='friends_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_friends_name', 'friends', ['name'], unique=False)
    op.create_index('ix_friends_id', 'friends', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_users_name', 'users', ['name'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('friend_attributes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('friend_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('attribute_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['attribute_id'], ['attributes.id'], name='friend_attributes_attribute_id_fkey'),
    sa.ForeignKeyConstraint(['friend_id'], ['friends.id'], name='friend_attributes_friend_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='friend_attributes_pkey')
    )
    op.create_index('ix_friend_attributes_id', 'friend_attributes', ['id'], unique=False)
    op.create_table('attributes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='attributes_pkey')
    )
    op.create_index('ix_attributes_name', 'attributes', ['name'], unique=True)
    op.create_index('ix_attributes_id', 'attributes', ['id'], unique=False)
    # ### end Alembic commands ###
