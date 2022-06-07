"""empty message

Revision ID: 82cbe7f75036
Revises: c9518647bb7a
Create Date: 2022-06-07 09:16:35.210522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82cbe7f75036'
down_revision = 'c9518647bb7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('film_user_id_fkey', 'film', type_='foreignkey')
    op.create_foreign_key(None, 'film', 'user', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'film', type_='foreignkey')
    op.create_foreign_key('film_user_id_fkey', 'film', 'user', ['user_id'], ['user_id'])
    # ### end Alembic commands ###