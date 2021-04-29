"""update retreat proposal table

Revision ID: 67dbe7217bcf
Revises: c37f22cddcba
Create Date: 2021-04-27 10:37:52.165151

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '67dbe7217bcf'
down_revision = 'c37f22cddcba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('retreats_proposals', sa.Column('flights_cost', sa.Integer(), nullable=False))
    op.add_column('retreats_proposals', sa.Column('lodging_cost', sa.Integer(), nullable=False))
    op.add_column('retreats_proposals', sa.Column('other_cost', sa.Integer(), nullable=False))
    op.alter_column('retreats_proposals', 'flight_time_avg', type_=sa.Numeric(precision=4, scale=2), postgresql_using='flight_time_avg::numeric(4,2)')
    op.drop_column('retreats_proposals', 'flights_estimate')
    op.drop_column('retreats_proposals', 'transportation_estimate')
    op.drop_column('retreats_proposals', 'lodging_estimate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('retreats_proposals', sa.Column('lodging_estimate', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('retreats_proposals', sa.Column('transportation_estimate', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('retreats_proposals', sa.Column('flights_estimate', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('retreats_proposals', 'flight_time_avg', type_=sa.Integer(), postgresql_using='flight_time_avg::integer')
    op.drop_column('retreats_proposals', 'other_cost')
    op.drop_column('retreats_proposals', 'lodging_cost')
    op.drop_column('retreats_proposals', 'flights_cost')
    # ### end Alembic commands ###