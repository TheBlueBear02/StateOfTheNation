"""Initial migration

Revision ID: fe75f0961c42
Revises: 
Create Date: 2024-11-24 13:15:09.992222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe75f0961c42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('non_parliament_members',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('twitter_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offices',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('info', sa.String(), nullable=True),
    sa.Column('minister_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parliament_members',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('party', sa.String(), nullable=True),
    sa.Column('additional_role', sa.String(), nullable=True),
    sa.Column('is_km', sa.Boolean(), nullable=False),
    sa.Column('is_coalition', sa.Boolean(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('twitter_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tweets',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('topic', sa.String(), nullable=True),
    sa.Column('twitter_id', sa.BigInteger(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('indexes',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('info', sa.String(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('office_id', sa.BigInteger(), nullable=False),
    sa.Column('is_kpi', sa.Boolean(), nullable=False),
    sa.Column('alert', sa.Boolean(), nullable=False),
    sa.Column('chart_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['office_id'], ['offices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ministers_history',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('party', sa.String(), nullable=True),
    sa.Column('start_date', sa.String(), nullable=False),
    sa.Column('office_id', sa.BigInteger(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['office_id'], ['offices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('indexes_data',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('index_id', sa.BigInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('value', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['index_id'], ['indexes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('indexes_data')
    op.drop_table('ministers_history')
    op.drop_table('indexes')
    op.drop_table('tweets')
    op.drop_table('parliament_members')
    op.drop_table('offices')
    op.drop_table('non_parliament_members')
    # ### end Alembic commands ###
