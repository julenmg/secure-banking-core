from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse
from app.models.task import Task


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    async def create_task(self, data: TaskCreate, user_id: int) -> TaskResponse:
        task = await self.repository.create(data.title, data.description, user_id)
        return TaskResponse.from_orm(task)
