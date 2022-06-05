"""empty message

Revision ID: c9518647bb7a
Revises: 1032756ac5fb
Create Date: 2022-06-05 10:12:20.597892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9518647bb7a'
down_revision = '1032756ac5fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('film', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'film', 'user', ['user_id'], ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'film', type_='foreignkey')
    op.drop_column('film', 'user_id')
    # ### end Alembic commands ###