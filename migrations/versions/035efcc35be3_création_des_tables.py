"""Création des tables

Revision ID: 035efcc35be3
Revises: 3766bed21626
Create Date: 2025-04-17 01:18:06.117234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '035efcc35be3'
down_revision = '3766bed21626'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('secret_key', sa.String(length=255), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('cart_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purchase_key', sa.String(length=100), nullable=False),
    sa.Column('qr_code_path', sa.String(length=120), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('purchase_key')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket')
    op.drop_table('cart_item')
    op.drop_table('user')
    op.drop_table('offer')
    # ### end Alembic commands ###
