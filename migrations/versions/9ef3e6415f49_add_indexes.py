"""Add indexes

Revision ID: 9ef3e6415f49
Revises: 6f494f9a37b6
Create Date: 2019-04-30 01:20:28.464861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef3e6415f49'
down_revision = '6f494f9a37b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_16469_apikey_id', table_name='apikey_permissions')
    op.drop_constraint('apikey_permissions_ibfk_1', 'apikey_permissions', type_='foreignkey')
    op.create_foreign_key(None, 'apikey_permissions', 'apikeys', ['apikey_id'], ['_id'], ondelete='CASCADE')
    op.drop_index('idx_16462_token', table_name='apikeys')
    op.create_unique_constraint(None, 'apikeys', ['token'])
    op.create_index('product_report_org_idx', 'product_reports', ['organisation'], unique=False)
    op.create_index('product_report_timestamp_idx', 'product_reports', ['timestamp'], unique=False)
    op.create_index('product_report_user_org_idx', 'product_reports', ['user', 'organisation'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('product_report_user_org_idx', table_name='product_reports')
    op.drop_index('product_report_timestamp_idx', table_name='product_reports')
    op.drop_index('product_report_org_idx', table_name='product_reports')
    op.drop_constraint(None, 'apikeys', type_='unique')
    op.create_index('idx_16462_token', 'apikeys', ['token'], unique=True)
    op.drop_constraint(None, 'apikey_permissions', type_='foreignkey')
    op.create_foreign_key('apikey_permissions_ibfk_1', 'apikey_permissions', 'apikeys', ['apikey_id'], ['_id'], onupdate='RESTRICT', ondelete='CASCADE')
    op.create_index('idx_16469_apikey_id', 'apikey_permissions', ['apikey_id'], unique=False)
    # ### end Alembic commands ###
