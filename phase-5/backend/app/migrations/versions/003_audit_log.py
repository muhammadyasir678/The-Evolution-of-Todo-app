"""
Migration script to create the AuditLog model
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003_audit_log'
down_revision = '002_advanced_features'
branch_labels = None
depends_on = None


def upgrade():
    # Create audit_log table
    op.create_table(
        'auditlog',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False, index=True),
        sa.Column('task_id', sa.Integer, nullable=True, index=True),
        sa.Column('action', sa.Enum('created', 'updated', 'deleted', 'completed', name='action_enum'), nullable=False),
        sa.Column('details', sa.Text, nullable=True),  # JSONB field for task data or changes
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('correlation_id', sa.String(255), nullable=True)
    )

    # Create indexes for performance
    op.create_index('ix_auditlog_user_id', 'auditlog', ['user_id'])
    op.create_index('ix_auditlog_task_id', 'auditlog', ['task_id'])
    op.create_index('ix_auditlog_timestamp', 'auditlog', ['timestamp'])


def downgrade():
    # Drop indexes
    op.drop_index('ix_auditlog_user_id')
    op.drop_index('ix_auditlog_task_id')
    op.drop_index('ix_auditlog_timestamp')

    # Drop audit_log table
    op.drop_table('auditlog')