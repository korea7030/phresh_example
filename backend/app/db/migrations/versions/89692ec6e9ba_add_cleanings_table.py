"""add cleanings table
Revision ID: 89692ec6e9ba
Revises: c382ebd06bc4
Create Date: 2023-03-16 08:00:31.099401
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '89692ec6e9ba'
down_revision = 'c382ebd06bc4'
branch_labels = None
depends_on = None

def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
    )
    

def upgrade() -> None:
    create_cleanings_table()


def downgrade() -> None:
    pass
