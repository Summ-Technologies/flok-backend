"""add flok_owner column to rfp table

Revision ID: 53282eab0220
Revises: 15bc5bc50c0f
Create Date: 2021-08-04 15:47:08.440288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53282eab0220'
down_revision = '15bc5bc50c0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lodging_proposal_requests', sa.Column('flok_owner', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lodging_proposal_requests', 'flok_owner')
    # ### end Alembic commands ###
