"""Last revision

Revision ID: 714634a09a06
Revises: f7db388a6659
Create Date: 2024-04-24 03:00:19.649123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '714634a09a06'
down_revision: Union[str, None] = 'f7db388a6659'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'time',
               existing_type=sa.DATE(),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'time',
               existing_type=sa.TIMESTAMP(),
               type_=sa.DATE(),
               existing_nullable=True)
    # ### end Alembic commands ###