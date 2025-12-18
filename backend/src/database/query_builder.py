from sqlalchemy.ext.asyncio import AsyncSession


class QueryBuilder:
    def __init__(self, session: AsyncSession, stmt):
        self.session = session
        self.stmt = stmt

    def where(self, condition, fn=None):
        if fn:
            self.stmt = self.stmt.where(fn())
        else:
            self.stmt = self.stmt.where(condition)
        return self

    def where_criterions(self, table, criterions):
        if not criterions:
            return self
        for c in criterions:
            self.stmt = self.stmt.where(c)
        return self

    def values(self, **values):
        self.stmt = self.stmt.values(**values)
        return self

    def order_by_with(self, table, sortby=None, descending=False):
        if sortby and hasattr(table, sortby):
            col = getattr(table, sortby)
            self.stmt = self.stmt.order_by(col.desc() if descending else col.asc())
        return self

    def limit(self, limit: int):
        self.stmt = self.stmt.limit(limit)
        return self

    def offset(self, offset: int):
        self.stmt = self.stmt.offset(offset)
        return self

    async def fetch(self):
        result = await self.session.execute(self.stmt)
        return result.scalars().all()

    async def fetchrow(self):
        result = await self.session.execute(self.stmt)
        return result.scalars().first()

    async def fetchpages(self):
        result = await self.session.execute(self.stmt)
        data = result.scalars().all()
        count = len(data)
        return data, count

    async def execute(self):
        await self.session.execute(self.stmt)
        await self.session.flush()
