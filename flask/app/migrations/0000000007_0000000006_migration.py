revision = "0000000007"
down_revision = "0000000006"


def upgrade(migration):
    # Add created_at and updated_at columns to task table
    migration.execute(
        """
        ALTER TABLE task 
        ADD COLUMN IF NOT EXISTS created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
        ADD COLUMN IF NOT EXISTS updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP;
    """
    )

    # Add created_at and updated_at columns to task_audit table
    migration.execute(
        """
        ALTER TABLE task_audit 
        ADD COLUMN IF NOT EXISTS created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
        ADD COLUMN IF NOT EXISTS updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP;
    """
    )

    migration.update_version_table(version=revision)


def downgrade(migration):
    # Remove created_at and updated_at columns from task table
    migration.execute(
        """
        ALTER TABLE task 
        DROP COLUMN IF EXISTS created_at,
        DROP COLUMN IF EXISTS updated_at;
    """
    )

    # Remove created_at and updated_at columns from task_audit table
    migration.execute(
        """
        ALTER TABLE task_audit 
        DROP COLUMN IF EXISTS created_at,
        DROP COLUMN IF EXISTS updated_at;
    """
    )

    migration.update_version_table(version=down_revision)
