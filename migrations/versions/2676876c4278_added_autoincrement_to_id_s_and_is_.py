"""Added autoincrement to id's and is_shown in index

Revision ID: 2676876c4278
Revises: 27d8573af53a
Create Date: 2025-03-04 14:15:20.157982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2676876c4278'
down_revision = '27d8573af53a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('indexes', sa.Column('is_shown', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('indexes', 'is_shown')
    # ### end Alembic commands ###
