"""limuting searches for free subscriptions

Revision ID: 30158b57bb92
Revises: 825791d04b9d
Create Date: 2024-09-22 20:57:19.797841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30158b57bb92'
down_revision = '825791d04b9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('query', sa.String(length=1000), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subscription_type', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('subscription_type')

    op.drop_table('search')
    # ### end Alembic commands ###
