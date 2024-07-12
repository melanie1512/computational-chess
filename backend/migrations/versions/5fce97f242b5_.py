"""empty message

Revision ID: 5fce97f242b5
Revises: 4e2a96a34ff0
Create Date: 2024-07-12 17:38:21.906574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fce97f242b5'
down_revision = '4e2a96a34ff0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pieces', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pieces', schema=None) as batch_op:
        batch_op.drop_column('value')

    # ### end Alembic commands ###