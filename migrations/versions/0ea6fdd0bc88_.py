"""empty message

Revision ID: 0ea6fdd0bc88
Revises: d1dcac92e041
Create Date: 2019-07-07 16:08:53.636926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea6fdd0bc88'
down_revision = 'd1dcac92e041'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('like', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'like')
    # ### end Alembic commands ###
