"""Force autoincrement on primary keys

Revision ID: 54d796749fe7
Revises: 2676876c4278
Create Date: 2025-03-05 12:37:40.426130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54d796749fe7'
down_revision = '2676876c4278'
branch_labels = None
depends_on = None


def upgrade():
    pass

# Downgrade function (undoes changes if needed)
def downgrade():
    pass  # Leave this empty if you don't need to reverse changes
