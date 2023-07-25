"""Restaurant Migration 2

Revision ID: 7f50321be430
Revises: 9825eeb9deee
Create Date: 2023-07-25 14:29:50.696718

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7f50321be430'
down_revision = '9825eeb9deee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.alter_column('operating_hours',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.alter_column('operating_hours',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###