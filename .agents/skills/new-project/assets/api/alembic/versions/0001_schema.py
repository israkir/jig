"""Create the {{db}} schema.

Revision ID: 0001
Revises:
Create Date: 2026-01-01

"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS {{db}} AUTHORIZATION {{db}}")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS {{db}} CASCADE")
