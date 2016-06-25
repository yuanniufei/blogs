"""empty message

Revision ID: f9cbc95f8b7f
Revises: 13b11dc52d6c
Create Date: 2016-06-15 13:51:54.260000

"""

# revision identifiers, used by Alembic.
revision = 'f9cbc95f8b7f'
down_revision = '13b11dc52d6c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'confirmed')
    ### end Alembic commands ###