"""create users table

Revision ID: 01f6ec21489b
Revises: d5bf14bd81a6
Create Date: 2022-01-07 22:20:21.995033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01f6ec21489b'
down_revision = 'd5bf14bd81a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id',sa.Integer(),nullable=False, primary_key=True),
        sa.Column('email', sa.String(),nullable=False),
        sa.Column('password', sa.String(),nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default = sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade():
    op.drop_table('users')
    pass
