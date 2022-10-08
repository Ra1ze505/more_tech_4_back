"""add_quest

Revision ID: 1955a2c4043e
Revises: 0649be7e6851
Create Date: 2022-10-08 19:46:47.948056

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "1955a2c4043e"
down_revision = "0649be7e6851"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("inventory", sa.Column("quest_books", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("inventory", "quest_books")
    # ### end Alembic commands ###
