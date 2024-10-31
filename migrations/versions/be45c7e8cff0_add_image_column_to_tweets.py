"""Add image column  to Tweets

Revision ID: be45c7e8cff0
Revises: d420c5ffbf90
Create Date: 2024-09-11 11:47:21.657354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be45c7e8cff0'
down_revision = 'd420c5ffbf90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('indexes', schema=None) as batch_op:
        batch_op.alter_column('chart_type',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('tweets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tweets', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('indexes', schema=None) as batch_op:
        batch_op.alter_column('chart_type',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###