"""Changed data format to string

Revision ID: 2659d5d7ef08
Revises: 3f82e60a65e0
Create Date: 2024-11-01 11:14:40.651966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2659d5d7ef08'
down_revision = '3f82e60a65e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ministers__history', 'start_date',
               existing_type=sa.DATE(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ministers__history', 'start_date',
               existing_type=sa.String(),
               type_=sa.DATE(),
               existing_nullable=False)
    # ### end Alembic commands ###