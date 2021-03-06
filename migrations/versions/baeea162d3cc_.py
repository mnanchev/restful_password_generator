"""empty message

Revision ID: baeea162d3cc
Revises: 911f30290e65
Create Date: 2021-12-31 10:51:05.483972

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "baeea162d3cc"
down_revision = "911f30290e65"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "secrets",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "secrets",
        "id",
        existing_type=sa.String(length=255),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
