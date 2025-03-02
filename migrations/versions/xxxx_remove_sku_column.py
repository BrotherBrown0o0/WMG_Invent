from alembic import op
import sqlalchemy as sa

def upgrade():
    op.drop_column('product', 'sku')

def downgrade():
    op.add_column('product', sa.Column('sku', sa.String(length=64), nullable=True)) 