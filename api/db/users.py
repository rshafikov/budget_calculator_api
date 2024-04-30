from models import TodoModel
from schemas import TodoBase
from database import AsyncSession
from sqlalchemy import select, update


async def get_task_by_desc(session: AsyncSession, task: TodoBase) -> TodoModel | None:
    result = await session.execute(select(TodoModel).filter(
        TodoModel.title == task.title,
        TodoModel.description == task.description)
    )
    return result.scalar_one_or_none()


async def get_task_by_id(session: AsyncSession, task_id: int) -> TodoModel | None:
    result = await session.execute(select(TodoModel).filter(TodoModel.id == task_id))
    return result.scalar_one_or_none()


def create_task(session: AsyncSession, task: TodoBase) -> TodoModel:
    new_task = TodoModel(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed
    )
    session.add(new_task)
    return new_task


async def get_all_tasks(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[TodoModel]:
    result = await session.execute(select(TodoModel).offset(skip).limit(limit))
    anw = [r for r in result.scalars().all()]
    return anw


async def update_task_in_db(session: AsyncSession, task_id: int, updated_task: TodoBase):
    await session.execute(
        update(TodoModel).filter(TodoModel.id == task_id).values(updated_task.model_dump()))
    await session.commit()
    task = await get_task_by_id(session, task_id=task_id)
    return task