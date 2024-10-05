from bot.src.repository.sqlalchemy_repository import SQLAlchemyRepository
from bot.src.models.establishment import Establishment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select



class EstablishmentRepository(SQLAlchemyRepository):

    model: Establishment = Establishment


    @classmethod
    async def find_all_limit_offset(cls, session: AsyncSession, limit: int, offset: int = 0):
        query = select(cls.model).limit(limit).offset(offset).order_by(cls.model.title)
        res = await session.execute(query)

        stmt_count = (
            select(func.count()).select_from(cls.model)
        )
        res_count = await session.execute(stmt_count)
        total_count: int = res_count.scalar()
        return res.scalars().all(), total_count
        
