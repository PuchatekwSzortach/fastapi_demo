"""initialize schema

Revision ID: f52fe22ab4fd
Revises:
Create Date: 2021-05-20 12:34:30.546068

"""
from sqlalchemy.sql.expression import null
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f52fe22ab4fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'user',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(320), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(72), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('is_superuser', sa.Boolean, default=False, nullable=False),
        sa.Column('is_verified', sa.Boolean, default=False, nullable=False),
        sa.Column('uniquifier', sa.String(length=36), nullable=True)
    )

    op.create_table(
        'items',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('owner_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(256), nullable=False),
    )


def downgrade():

    raise NotImplementedError()
