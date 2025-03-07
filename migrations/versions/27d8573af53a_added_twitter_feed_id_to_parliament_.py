"""Added twitter feed id to parliament members table and news feed id to index table

Revision ID: 27d8573af53a
Revises: 2826df0a03df
Create Date: 2025-02-25 12:45:25.752214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27d8573af53a'
down_revision = '2826df0a03df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('indexes', sa.Column('news_feed_id', sa.String(), nullable=True))
    op.add_column('parliament_members', sa.Column('twitter_feed_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('parliament_members', 'twitter_feed_id')
    op.drop_column('indexes', 'news_feed_id')
    # ### end Alembic commands ###
