revision = "0000000006"
down_revision = "0000000005"


def upgrade(migration):
    # write migration here
    migration.create_table(
        "task",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "person_id" varchar(32) NOT NULL,
            "title" varchar(255) NOT NULL,
            "description" text DEFAULT NULL,
            "is_completed" boolean DEFAULT false,
            "created_at" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY ("entity_id")
        """,
    )
    migration.add_index("task", "task_person_id_ind", "person_id")

    # Create the "task_audit" table
    migration.create_table(
        "task_audit",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "person_id" varchar(32) NOT NULL,
            "title" varchar(255) NOT NULL,
            "description" text DEFAULT NULL,
            "is_completed" boolean DEFAULT false,
            "created_at" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY ("entity_id", "version")
        """,
    )

    migration.update_version_table(version=revision)


def downgrade(migration):
    # write migration here
    migration.drop_table(table_name="task")
    migration.drop_table(table_name="task_audit")
    migration.update_version_table(version=down_revision)
