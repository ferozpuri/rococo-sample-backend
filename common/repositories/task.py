from common.repositories.base import BaseRepository
from common.models.task import Task


class TaskRepository(BaseRepository):
    MODEL = Task

    def __init__(self, db_adapter, message_adapter=None, queue_name="", user_id=None):
        super().__init__(db_adapter, message_adapter, queue_name, user_id)
        self.model = self.MODEL

    def get_all(self, query=None):
        """Get all tasks with optional query parameters"""
        if query is None:
            query = {}
        return self.get_many(query)

    def get_by_id(self, task_id):
        """Get a task by its ID"""
        return self.get_one({"entity_id": task_id})

    def create(self, task_data):
        """Create a new task"""
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
