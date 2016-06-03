"""empty message

Revision ID: ba7340bc6974
Revises: 5c5ddb755e41
Create Date: 2016-06-04 00:25:34.329000

"""

# revision identifiers, used by Alembic.
revision = 'ba7340bc6974'
down_revision = '5c5ddb755e41'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column(u'posts', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'categories', ['category_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column(u'posts', 'category_id')
    op.drop_table('categories')
    ### end Alembic commands ###
