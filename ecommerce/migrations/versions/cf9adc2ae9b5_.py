"""empty message

Revision ID: cf9adc2ae9b5
Revises: 
Create Date: 2023-03-12 12:47:42.005483

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cf9adc2ae9b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category_image', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.MEDIUMBLOB(),
               type_=sa.LargeBinary(length=10485759),
               existing_nullable=False)

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=True))

    with op.batch_alter_table('product_image', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.MEDIUMBLOB(),
               type_=sa.LargeBinary(length=10485759),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_image', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=10485759),
               type_=mysql.MEDIUMBLOB(),
               existing_nullable=False)

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('type')

    with op.batch_alter_table('category_image', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=10485759),
               type_=mysql.MEDIUMBLOB(),
               existing_nullable=False)

    # ### end Alembic commands ###
