from common.repositories.base import BaseRepository
from common.models.task import Task
import uuid
from datetime import datetime


class TaskRepository(BaseRepository):
    MODEL = Task

    def __init__(self, db_adapter, message_adapter=None, queue_name="", user_id=None):
        super().__init__(db_adapter, message_adapter, queue_name, user_id)
        self.model = self.MODEL

    def get_all(self, query=None, offset: int = 0, limit: int = None):
        """Get all tasks with optional query parameters and pagination"""
        if query is None:
            query = {}

        # Add ORDER BY clause to sort by created_at in descending order
        # order_by = "ORDER BY created_at DESC"
        # return self.get_many(query, offset=offset, limit=limit)

        # Build the WHERE clause from the query dict
        where_conditions = []
        params = []
        for key, value in query.items():
            where_conditions.append(f"{key} = %s")
            params.append(value)

        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

        # Build the complete SQL query with ordering
        sql = f"""
            SELECT *
            FROM task
            WHERE {where_clause}
            ORDER BY created_at DESC
        """

        # Add pagination if specified
        if limit is not None:
            sql += " LIMIT %s"
            params.append(limit)
        if offset > 0:
            sql += " OFFSET %s"
            params.append(offset)

        # Execute the query
        with self.adapter:
            results = self.adapter.execute_query(sql, tuple(params))
            return [self.MODEL(**result) for result in results]

    def get_by_id(self, task_id):
        """Get a task by its ID"""
        return self.get_one({"entity_id": task_id})

    def create(self, task_data):
        """Create a new task"""
        # Initialize version fields
        task_data["version"] = str(uuid.uuid4()).replace("-", "")
        task_data["previous_version"] = "00000000000000000000000000000000"
        task_data["active"] = True
        task_data["changed_by_id"] = (
            task_data.get("person_id") or self.user_id or "system"
        )
        task_data["changed_on"] = datetime.utcnow()

        # Create the task instance
        task = self.MODEL(**task_data)
        return self.save(task)

    def update(self, task_id, task_data):
        """Update an existing task"""
        task = self.get_by_id(task_id)
        if task:
            for key, value in task_data.items():
                setattr(task, key, value)
            return self.save(task)
        return None

    def delete(self, task_id):
        """Delete a task"""
        task = self.get_by_id(task_id)
        if task:
            return super().delete(task)
        return None

    def count(self, filter_dict):
        """Count records matching the given filter"""
        results = self.get_many(filter_dict)
        return len(results)
