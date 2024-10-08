"""add_allow_ids_table

Revision ID: 4e307563ce01
Revises: 6a3482d4534b
Create Date: 2024-09-04 16:52:15.855190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e307563ce01'
down_revision: Union[str, None] = '6a3482d4534b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('allowed_ids',
    sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('allowed_ids')
    # ### end Alembic commands ###
