"""init user and auth tables

Revision ID: baed3daf19ae
Revises: 
Create Date: 2021-07-26 11:50:45.465544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baed3daf19ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('users_login_ids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('login_id', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_login_ids_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users_login_ids')),
    sa.UniqueConstraint('login_id', name=op.f('uq_users_login_ids_login_id'))
    )
    op.create_table('users_login_providers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(), nullable=False),
    sa.Column('unique_id', sa.String(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_login_providers_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users_login_providers'))
    )
    op.create_table('users_login_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('login_token', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_login_tokens_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users_login_tokens')),
    sa.UniqueConstraint('login_token', name=op.f('uq_users_login_tokens_login_token'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_login_tokens')
    op.drop_table('users_login_providers')
    op.drop_table('users_login_ids')
    op.drop_table('users')
    # ### end Alembic commands ###
