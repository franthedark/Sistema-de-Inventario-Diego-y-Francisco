"""Añadir nuevos campos totales compras y ventas

Revision ID: d1d33a92dc13
Revises: a119f6a1c91a
Create Date: 2024-12-05 02:39:08.662707

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'd1d33a92dc13'
down_revision: Union[str, None] = 'a119f6a1c91a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Obtener el inspector de las tablas
    inspector = inspect(op.get_bind())

    # Verificar si las columnas ya existen en la tabla 'compras'
    columns_compras = [col['name'] for col in inspector.get_columns('compras')]
    if 'total_productos_vendidos' not in columns_compras:
        op.add_column('compras', sa.Column('total_productos_vendidos', sa.Integer(), nullable=True))
    if 'total_costo_productos' not in columns_compras:
        op.add_column('compras', sa.Column('total_costo_productos', sa.Float(), nullable=True))

    # Verificar si las columnas ya existen en la tabla 'ventas'
    columns_ventas = [col['name'] for col in inspector.get_columns('ventas')]
    if 'total_productos_vendidos' not in columns_ventas:
        op.add_column('ventas', sa.Column('total_productos_vendidos', sa.Integer(), nullable=True))
    if 'total_costo_productos' not in columns_ventas:
        op.add_column('ventas', sa.Column('total_costo_productos', sa.Float(), nullable=True))
    if 'ganancias' not in columns_ventas:
        op.add_column('ventas', sa.Column('ganancias', sa.Float(), nullable=True))
        
def downgrade() -> None:
    # Volver a modificar las columnas a su estado anterior
    op.alter_column('ventas', 'total', existing_type=sa.FLOAT(), nullable=True)
    op.drop_column('ventas', 'ganancias')
    op.drop_column('ventas', 'total_costo_productos')
    op.drop_column('ventas', 'total_productos_vendidos')
    op.alter_column('compras', 'total', existing_type=sa.FLOAT(), nullable=True)
    op.drop_column('compras', 'total_costo_productos')
    op.drop_column('compras', 'total_productos_vendidos')