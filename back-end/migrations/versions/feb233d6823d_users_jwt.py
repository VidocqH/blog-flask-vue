"""users jwt

Revision ID: feb233d6823d
Revises: 9ed34dd5ebec
Create Date: 2020-12-04 21:47:54.513100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feb233d6823d'
down_revision = '9ed34dd5ebec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('token_expiration')
        batch_op.drop_column('token')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.VARCHAR(length=32), nullable=True))
        batch_op.add_column(sa.Column('token_expiration', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###
