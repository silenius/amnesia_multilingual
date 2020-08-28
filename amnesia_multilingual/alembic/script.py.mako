"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from pathlib import Path
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

migration_path = Path(__file__)
migration_sql_path = migration_path.parent.parent / 'sql'
migration_sql_file = migration_path.with_suffix('.sql').name

upgrade_sql = migration_sql_path / 'upgrade' / migration_sql_file
downgrade_sql = migration_sql_path / 'downgrade' / migration_sql_file

def upgrade():
    ${upgrades if upgrades else "pass"}

def downgrade():
    ${downgrades if downgrades else "pass"}
