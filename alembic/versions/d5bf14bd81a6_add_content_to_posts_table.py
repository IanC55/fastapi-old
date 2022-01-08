"""add content to posts table

Revision ID: d5bf14bd81a6
Revises: e8b690b441a8
Create Date: 2022-01-07 20:01:48.718515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5bf14bd81a6'
down_revision = 'e8b690b441a8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
