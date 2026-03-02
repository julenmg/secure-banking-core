from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.core.database import get_db
from app.models.task import Task  # Añadir la importación de Task
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService  # Añadir la importación de TaskService
from app.schemas.task import TaskCreate, TaskResponse


router = APIRouter()


def _get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(TaskRepository(db))


@router.post("/tasks", response_model=TaskResponse, status_code=HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    user_id: int,
    service: TaskService = Depends(_get_task_service),
):
    task = await service.create_task(data, user_id)
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await TaskRepository(db).get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse.from_orm(task)


@router.get("/users/{user_id}/tasks", response_model=list[TaskResponse])
async def get_tasks_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    tasks = await TaskRepository(db).get_by_user_id(user_id)
    return [TaskResponse.from_orm(task) for task in tasks]
