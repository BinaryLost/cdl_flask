"""empty message

Revision ID: c0ff54b0e468
Revises: cf9adc2ae9b5
Create Date: 2023-03-12 14:49:15.455686

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c0ff54b0e468'
down_revision = 'cf9adc2ae9b5'
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
        batch_op.add_column(sa.Column('gender', sa.String(length=50), nullable=False))
        batch_op.alter_column('active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('price',
               existing_type=mysql.FLOAT(),
               nullable=False)

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
        batch_op.alter_column('price',
               existing_type=mysql.FLOAT(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
        batch_op.drop_column('gender')

    with op.batch_alter_table('category_image', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=10485759),
               type_=mysql.MEDIUMBLOB(),
               existing_nullable=False)

    # ### end Alembic commands ###
