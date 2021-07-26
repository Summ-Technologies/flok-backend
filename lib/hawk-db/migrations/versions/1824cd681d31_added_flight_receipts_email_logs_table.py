"""added flight receipts email logs table

Revision ID: 1824cd681d31
Revises: 6f8d27d162eb
Create Date: 2021-07-15 01:18:00.014449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1824cd681d31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_id', sa.String(), nullable=False),
    sa.Column('date_added', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_email_logs'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_logs')
    # ### end Alembic commands ###
