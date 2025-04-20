from flask_restx import Namespace, Resource, reqparse
from flask import request
from app.helpers.response import (
    get_success_response,
    get_failure_response,
    parse_request_body,
    validate_required_fields,
)
from common.app_config import config
from common.services import TaskService
from app.helpers.decorators import login_required

# Create the task blueprint
task_api = Namespace("tasks", description="Task-related APIs")

# Request parser for filtering tasks
task_filter_parser = reqparse.RequestParser()
task_filter_parser.add_argument(
    "is_completed", type=int, required=False, help="Filter tasks by completion status"
)
task_filter_parser.add_argument(
    "page", type=int, required=False, default=1, help="Page number"
)
task_filter_parser.add_argument(
    "per_page", type=int, required=False, default=2, help="Number of items per page"
)


@task_api.route("/")
class Tasks(Resource):
    @login_required()
    def get(self, person):
        """Get all tasks for the current user with optional filter and pagination"""
        args = task_filter_parser.parse_args()
        is_completed = args.get("is_completed")
        page = args.get("page")
        per_page = args.get("per_page")

        if is_completed is not None:
            is_completed = True if is_completed == 1 else False

        task_service = TaskService(config)
        tasks = task_service.get_tasks_by_person(
            person.entity_id, is_completed, offset=(page - 1) * per_page, limit=per_page
        )
        total_tasks = task_service.count_tasks_by_person(person.entity_id, is_completed)

        return get_success_response(
            tasks=[task.as_dict() for task in tasks],
            pagination={
                "total": total_tasks,
                "page": page,
                "per_page": per_page,
                "total_pages": (total_tasks + per_page - 1) // per_page,
            },
        )

    @login_required()
    def post(self, person):
        """Create a new task"""
        parsed_body = parse_request_body(request, ["title", "description"])
        validate_required_fields(parsed_body)

        task_service = TaskService(config)
        task = task_service.create_task(
            title=parsed_body["title"],
            description=parsed_body.get("description"),
            person_id=person.entity_id,
        )
        return get_success_response(
            message="Task created successfully.", task=task.as_dict()
        )


@task_api.route("/<string:task_id>")
class Task(Resource):
    @login_required()
    def get(self, person, task_id):
        """Get a specific task"""
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)

        if not task:
            return get_failure_response(message="Task not found")

        if task.person_id != person.entity_id:
            return get_failure_response(message="Unauthorized access to task")

        return get_success_response(task=task.as_dict())

    @login_required()
    def patch(self, person, task_id):
        """Update only the completion status of a task"""
        parsed_body = parse_request_body(request, ["is_completed"])
        validate_required_fields(parsed_body)

        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)

        if not task:
            return get_failure_response(message="Task not found")

        if task.person_id != person.entity_id:
            return get_failure_response(message="Unauthorized access to task")

        updated_task = task_service.update_task(
            task_id=task_id, is_completed=parsed_body["is_completed"]
        )

        if not updated_task:
            return get_failure_response(message="Failed to update task")

        return get_success_response(
            message="Task completion status updated successfully.",
            task=updated_task.as_dict(),
        )

    @login_required()
    def put(self, person, task_id):
        """Update a task"""
        parsed_body = parse_request_body(
            request, ["title", "description", "is_completed"]
        )
        # Only validate required fields (title and description)
        validate_required_fields(
            {
                "title": parsed_body.get("title"),
                "description": parsed_body.get("description"),
            }
        )

        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)

        if not task:
            return get_failure_response(message="Task not found")

        if task.person_id != person.entity_id:
            return get_failure_response(message="Unauthorized access to task")

        updated_task = task_service.update_task(
            task_id=task_id,
            title=parsed_body.get("title"),
            description=parsed_body.get("description"),
            is_completed=parsed_body.get(
                "is_completed"
            ),  # This will be None if not provided
        )

        if not updated_task:
            return get_failure_response(message="Failed to update task")

        return get_success_response(
            message="Task updated successfully.", task=updated_task.as_dict()
        )

    @login_required()
    def delete(self, person, task_id):
        """Delete a task"""
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)

        if not task:
            return get_failure_response(message="Task not found")

        if task.person_id != person.entity_id:
            return get_failure_response(message="Unauthorized access to task")

        if not task_service.delete_task(task_id):
            return get_failure_response(message="Failed to delete task")

        return get_success_response(message="Task deleted successfully.")
