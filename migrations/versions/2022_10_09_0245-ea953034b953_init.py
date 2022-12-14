"""init

Revision ID: ea953034b953
Revises:
Create Date: 2022-10-09 02:45:42.779193

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ea953034b953"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
    # ### end Alembic commands ###
