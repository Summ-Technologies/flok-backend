"""Added company_name column to rfp form

Revision ID: f07f50188626
Revises: bc5a7a9b0550
Create Date: 2021-08-02 08:30:36.008181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f07f50188626'
down_revision = 'bc5a7a9b0550'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lodging_proposal_requests', sa.Column('company_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lodging_proposal_requests', 'company_name')
    # ### end Alembic commands ###
