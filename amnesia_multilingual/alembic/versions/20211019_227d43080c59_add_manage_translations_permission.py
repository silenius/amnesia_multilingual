"""add manage_translations permission

Revision ID: 227d43080c59
Revises: f78c46839e11
Create Date: 2021-10-19 12:00:46.466726

"""
from pathlib import Path
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '227d43080c59'
down_revision = 'f78c46839e11'
branch_labels = None
depends_on = None

migration_path = Path(__file__)
migration_sql_path = migration_path.parent.parent / 'sql'
migration_sql_file = migration_path.with_suffix('.sql').name

upgrade_sql = migration_sql_path / 'upgrade' / migration_sql_file
downgrade_sql = migration_sql_path / 'downgrade' / migration_sql_file

def upgrade():
    print('===>>> Executing ', upgrade_sql)
    with open(upgrade_sql, 'r') as fp:
        op.execute(fp.read())

def downgrade():
    print('===>>> Executing ', downgrade_sql)
    with open(downgrade_sql, 'r') as fp:
        op.execute(fp.read())
