"""empty message

Revision ID: 440c89b335f2
Revises: 63abadb6da8e
Create Date: 2021-04-30 14:02:55.378076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '440c89b335f2'
down_revision = '63abadb6da8e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('liidit', sa.Column('todennakoisyys', sa.Numeric(precision=3, scale=2),
        existing_server_default=None,
        nullable=False, 
        server_default=None))


def downgrade():
    pass
