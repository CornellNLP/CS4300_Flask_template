"""empty message

Revision ID: 20c5cfdc4de8
Revises: 290a15fe89a6
Create Date: 2020-04-11 21:40:37.586576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20c5cfdc4de8'
down_revision = '290a15fe89a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jokes', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('jokes', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('jokes', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.drop_column('jokes', 'hello')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jokes', sa.Column('hello', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('jokes', 'updated_at')
    op.drop_column('jokes', 'id')
    op.drop_column('jokes', 'created_at')
    # ### end Alembic commands ###