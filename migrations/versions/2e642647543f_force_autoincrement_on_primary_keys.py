"""Force autoincrement on primary keys

Revision ID: 2e642647543f
Revises: 0071d8ed9210
Create Date: 2025-03-05 14:08:16.049492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e642647543f'
down_revision = '0071d8ed9210'
branch_labels = None
depends_on = None


def upgrade():
    # Create new tables with updated schema
    op.create_table(
        'indexes',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('info', sa.String(), nullable=True),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('office_id', sa.Integer(), sa.ForeignKey('offices.id'), nullable=False),
        sa.Column('is_kpi', sa.Boolean(), default=False, nullable=False),
        sa.Column('alert', sa.Boolean(), default=False, nullable=False),
        sa.Column('chart_type', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('news_feed_id', sa.String(), nullable=True),
        sa.Column('is_shown', sa.Boolean(), default=True, nullable=True)
    )

    op.create_table(
        'indexes_data',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('index_id', sa.Integer(), sa.ForeignKey('indexes.id'), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False)
    )

    op.create_table(
        'ministers_history',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('party', sa.String(), nullable=True),
        sa.Column('start_date', sa.String(), nullable=False),
        sa.Column('office_id', sa.Integer(), sa.ForeignKey('offices.id'), nullable=False),
        sa.Column('image', sa.String(), nullable=True)
    )

    op.create_table(
        'offices',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('info', sa.String(), nullable=True),
        sa.Column('minister_id', sa.Integer(), nullable=False),
        sa.Column('news_feed_id', sa.String(), nullable=True)
    )

    op.create_table(
        'tweets',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('time', sa.String(), nullable=False),
        sa.Column('topic', sa.String(), nullable=True),
        sa.Column('twitter_id', sa.Integer(), nullable=False),
        sa.Column('image', sa.String(), nullable=True)
    )

    op.create_table(
        'parliament_members',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('party', sa.String(), nullable=True),
        sa.Column('additional_role', sa.String(), nullable=True),
        sa.Column('is_km', sa.Boolean(), default=False, nullable=False),
        sa.Column('is_coalition', sa.Boolean(), default=False, nullable=False),
        sa.Column('image', sa.String(), nullable=True),
        sa.Column('twitter_id', sa.String(), nullable=True),
        sa.Column('twitter_feed_id', sa.String(), nullable=True)
    )

    op.create_table(
        'non_parliament_members',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('start_date', sa.String(), nullable=True),
        sa.Column('finish_date', sa.String(), nullable=True),
        sa.Column('image', sa.String(), nullable=True),
        sa.Column('twitter_id', sa.String(), nullable=True),
        sa.Column('appointed_by', sa.String(), nullable=True)
    )

    op.create_table(
        'office_branches',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('office_id', sa.Integer(), sa.ForeignKey('offices.id'), nullable=False),
        sa.Column('image', sa.String(), nullable=True)
    )

    # Data Migration (assuming old tables are named with '_old' suffix)
    op.execute("INSERT INTO indexes (id, name, info, icon, office_id, is_kpi, alert, chart_type, source, news_feed_id, is_shown) SELECT id, name, info, icon, office_id, is_kpi, alert, chart_type, source, news_feed_id, is_shown FROM indexes_old")
    op.execute("INSERT INTO indexes_data (id, index_id, label, value) SELECT id, index_id, label, value FROM indexes_data_old")
    op.execute("INSERT INTO ministers_history (id, name, party, start_date, office_id, image) SELECT id, name, party, start_date, office_id, image FROM ministers_history_old")
    op.execute("INSERT INTO offices (id, name, info, minister_id, news_feed_id) SELECT id, name, info, minister_id, news_feed_id FROM offices_old")
    op.execute("INSERT INTO tweets (id, text, date, time, topic, twitter_id, image) SELECT id, text, date, time, topic, twitter_id, image FROM tweets_old")
    op.execute("INSERT INTO parliament_members (id, name, party, additional_role, is_km, is_coalition, image, twitter_id, twitter_feed_id) SELECT id, name, party, additional_role, is_km, is_coalition, image, twitter_id, twitter_feed_id FROM parliament_members_old")
    op.execute("INSERT INTO non_parliament_members (id, name, role, start_date, finish_date, image, twitter_id, appointed_by) SELECT id, name, role, start_date, finish_date, image, twitter_id, appointed_by FROM non_parliament_members_old")
    op.execute("INSERT INTO office_branches (id, name, office_id, image) SELECT id, name, office_id, image FROM office_branches_old")

    # Drop old tables
    op.drop_table('indexes_old')
    op.drop_table('indexes_data_old')
    op.drop_table('ministers_history_old')
    op.drop_table('offices_old')
    op.drop_table('tweets_old')
    op.drop_table('parliament_members_old')
    op.drop_table('non_parliament_members_old')
    op.drop_table('office_branches_old')


def downgrade():
    pass
