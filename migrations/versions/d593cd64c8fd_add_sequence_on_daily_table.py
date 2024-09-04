"""

Revision ID: d593cd64c8fd
Revises: 4e307563ce01
Create Date: 2024-09-04 20:17:58.840885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd593cd64c8fd'
down_revision: Union[str, None] = '4e307563ce01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создание последовательности
    op.execute("CREATE SEQUENCE daily_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;")

    # Изменение столбца id для использования этой последовательности
    op.alter_column('daily', 'id',
                    existing_type=sa.BigInteger(),
                    server_default=sa.text("nextval('daily_id_seq'::regclass)"),
                    existing_nullable=False,
                    autoincrement=True)

def downgrade():
    # Удаление изменения (откат)
    op.alter_column('daily', 'id',
                    existing_type=sa.BigInteger(),
                    server_default=None,
                    existing_nullable=False,
                    autoincrement=True)

    # Удаление последовательности
    op.execute("DROP SEQUENCE daily_id_seq;")
