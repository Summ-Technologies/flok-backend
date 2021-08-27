"""add flok admin flag to rfp table

Revision ID: 27fc55864b9e
Revises: c324dbc4a0f8
Create Date: 2021-08-27 14:09:33.796184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27fc55864b9e'
down_revision = 'c324dbc4a0f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lodging_proposal_requests', sa.Column('created_by_flok_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lodging_proposal_requests', 'created_by_flok_admin')
    # ### end Alembic commands ###