"""Initial empty migration

Revision ID: 5abb52233c92
Revises: 6392e01e6765
Create Date: 2025-08-04 23:09:32.501971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5abb52233c92'
down_revision: Union[str, Sequence[str], None] = '6392e01e6765'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
