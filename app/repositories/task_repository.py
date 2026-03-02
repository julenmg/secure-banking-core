from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models.task import Task
from app.models.user import User


class TaskRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, task_id: int) -> Task | None:
        query = select(Task).where(Task.id == task_id).options(joinedload(Task.user))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_user_id(self, user_id: int) -> list[Task]:
        query = select(Task).where(Task.user_id == user_id).options(joinedload(Task.user))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, title: str, description: str, user_id: int) -> Task:
        task = Task(title=title, description=description, user_id=user_id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
