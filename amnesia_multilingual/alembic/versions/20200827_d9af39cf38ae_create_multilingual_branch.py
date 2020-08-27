"""create multilingual branch

Revision ID: d9af39cf38ae
Revises:
Create Date: 2020-08-27 14:18:50.283977

"""
from pathlib import Path
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9af39cf38ae'
down_revision = None
branch_labels = ('multilingual',)
depends_on = ('e025de45166e', )

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
