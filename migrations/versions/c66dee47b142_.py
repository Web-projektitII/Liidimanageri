"""empty message

Revision ID: c66dee47b142
Revises: 440c89b335f2
Create Date: 2021-04-30 14:21:47.873776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c66dee47b142'
down_revision = '440c89b335f2'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('liidit', sa.Column('todennakoisyys', sa.Numeric(precision=3, scale=2),
        existing_server_default=None,
        nullable=False, 
        server_default=None))

def downgrade():
    pass
