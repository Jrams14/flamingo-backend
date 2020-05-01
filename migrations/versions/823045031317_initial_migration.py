"""Initial migration


Revision ID: 823045031317
Revises: 61e59acc6816
Create Date: 2020-04-28 03:17:00.332834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '823045031317'
down_revision = '61e59acc6816'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('following')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('following',
    sa.Column('user1', sa.INTEGER(), nullable=False),
    sa.Column('user2', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user1'], ['user.public_id'], ),
    sa.ForeignKeyConstraint(['user2'], ['user.public_id'], ),
    sa.PrimaryKeyConstraint('user1', 'user2')
    )
    # ### end Alembic commands ###