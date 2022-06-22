"""empty message

Revision ID: 89902bb37e77
Revises: c66dee47b142
Create Date: 2021-04-30 14:23:54.088838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89902bb37e77'
down_revision = 'c66dee47b142'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('liidit', 'todennakoisyys', 
        type_=sa.Numeric(precision=3, scale=2),
        existing_type=sa.Numeric(precision=2, scale=2), 
        nullable=True,
        existing_nullable=True,
        existing_server_default=None,
        server_default='0.00')


def downgrade():
    op.alter_column('liidit', 'todennakoisyys', 
        type_=sa.Numeric(precision=2, scale=2),
        existing_type=sa.Numeric(precision=3, scale=2), 
        nullable=True,
        existing_nullable=True,
        existing_server_default=0.0,
        server_default=None)