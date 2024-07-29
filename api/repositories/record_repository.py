from datetime import date
from typing import Sequence

from sqlalchemy import select

from api.db.models import RecordModel
from api.repositories.base_repository import Repository


class RecordRepository(Repository):
    model = RecordModel

    async def filter_by_date(
            self, _from: date | None = None, _to: date | None = None, **kwargs
    ) -> Sequence[RecordModel]:
        if _to is None:
            _to = date.max

        if _from is None:
            _from = date.min

        q = select(self.model).where(
            self.model.created_at.between(_from, _to)
        ).filter_by(**kwargs)
        r = await self.session.execute(q)
        return r.scalars().all()
