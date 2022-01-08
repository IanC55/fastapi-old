"""add 2 columns to posts table

Revision ID: eff3e6085152
Revises: d4da1c3a9bf4
Create Date: 2022-01-07 22:47:00.139666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eff3e6085152'
down_revision = 'd4da1c3a9bf4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
        sa.Column('published',sa.Boolean(),nullable=False, server_default = 'TRUE'))
    op.add_column('posts',    
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default = sa.text('now()'), nullable=False)
    )
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
