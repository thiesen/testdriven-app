"""empty message

Revision ID: 084e620336fc
Revises: 77f8df700b09
Create Date: 2018-06-20 18:16:25.351336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '084e620336fc'
down_revision = '77f8df700b09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
