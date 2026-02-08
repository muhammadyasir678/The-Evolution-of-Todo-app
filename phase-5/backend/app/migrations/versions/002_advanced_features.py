"""
Migration script to add advanced features fields to the Task model
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_advanced_features'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to the task table
    op.add_column('task', sa.Column('priority', sa.Enum('high', 'medium', 'low', name='priority_enum'), server_default='medium'))
    op.add_column('task', sa.Column('tags', sa.String))  # Will store as JSON string
    op.add_column('task', sa.Column('due_date', sa.DateTime))
    op.add_column('task', sa.Column('reminder_time', sa.DateTime))
    op.add_column('task', sa.Column('recurrence_pattern', sa.Enum('daily', 'weekly', 'monthly', name='recurrence_enum')))
    op.add_column('task', sa.Column('recurrence_interval', sa.Integer))
    op.add_column('task', sa.Column('parent_task_id', sa.Integer))

    # Create indexes for performance
    op.create_index('ix_task_priority', 'task', ['priority'])
    op.create_index('ix_task_due_date', 'task', ['due_date'])
    op.create_index('ix_task_parent_task_id', 'task', ['parent_task_id'])


def downgrade():
    # Drop indexes
    op.drop_index('ix_task_priority')
    op.drop_index('ix_task_due_date')
    op.drop_index('ix_task_parent_task_id')

    # Drop columns
    op.drop_column('task', 'parent_task_id')
    op.drop_column('task', 'recurrence_interval')
    op.drop_column('task', 'recurrence_pattern')
    op.drop_column('task', 'reminder_time')
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'tags')
    op.drop_column('task', 'priority')