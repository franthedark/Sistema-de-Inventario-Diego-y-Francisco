"""Agregar campo total

Revision ID: a119f6a1c91a
Revises: 20763577211a
Create Date: 2024-12-04 23:30:02.921652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a119f6a1c91a'
down_revision: Union[str, None] = '20763577211a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('compras', sa.Column('total', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('compras', 'total')
    # ### end Alembic commands ###
