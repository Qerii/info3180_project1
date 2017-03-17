"""empty message

Revision ID: 886764b3b039
Revises: a1e1d4b8faa5
Create Date: 2017-03-14 18:12:14.929717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '886764b3b039'
down_revision = 'a1e1d4b8faa5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('file', sa.String(length=80), nullable=True))
    op.add_column('user_profile', sa.Column('userid', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'user_profile', ['username'])
    op.drop_column('user_profile', 'image')
    op.drop_column('user_profile', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('user_profile', sa.Column('image', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user_profile', type_='unique')
    op.drop_column('user_profile', 'userid')
    op.drop_column('user_profile', 'file')
    # ### end Alembic commands ###
