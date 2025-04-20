from common.repositories.factory import RepositoryFactory, RepoType
from common.models.task import Task
import uuid
from datetime import datetime


class TaskService:
    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.task_repo = self.repository_factory.get_repository(RepoType.TASK)

    def create_task(self, title: str, person_id: str, description: str = None) -> Task:
        """Create a new task.

        Args:
            title (str): The title of the task.
            person_id (str): The ID of the person assigned to the task.
            description (str, optional): The description of the task. Defaults to None.

        Returns:
            Task: The created task.
        """
        task_data = {
            "title": title,
            "description": description,
            "person_id": person_id,
            "is_completed": False,
        }
        return self.task_repo.create(task_data)

    def save_task(self, task: Task) -> Task:
        return self.task_repo.save(task)

    def get_task_by_id(self, task_id: str) -> Task:
        return self.task_repo.get_by_id(task_id)

    def get_tasks_by_person(
        self,
        person_id: str,
        is_completed: bool = None,
        offset: int = 0,
        limit: int = None,
    ) -> list:
        query = {"person_id": person_id}
        if is_completed is not None:
            query["is_completed"] = is_completed
        return self.task_repo.get_all(query, offset=offset, limit=limit)

    def count_tasks_by_person(self, person_id: str, is_completed: bool = None) -> int:
        query = {"person_id": person_id}
        if is_completed is not None:
            query["is_completed"] = is_completed
        return self.task_repo.count(query)

    def update_task(
        self,
        task_id: str,
        title: str = None,
        description: str = None,
        is_completed: bool = None,
    ) -> Task:
        task_data = {}
        if title is not None:
            task_data["title"] = title
        if description is not None:
            task_data["description"] = description
        if is_completed is not None:
            task_data["is_completed"] = is_completed

        return self.task_repo.update(task_id, task_data)

    def delete_task(self, task_id: str) -> bool:
        return self.task_repo.delete(task_id) is not None

    def get_all_tasks(self) -> list:
        return self.task_repo.get_all({})

    def mark_task_completed(self, task_id: str) -> Task:
        return self.update_task(task_id, is_completed=True)

    def get_completed_tasks(self, person_id: str) -> list:
        return self.get_tasks_by_person(person_id, is_completed=True)

    def get_pending_tasks(self, person_id: str) -> list:
        return self.get_tasks_by_person(person_id, is_completed=False)
