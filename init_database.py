from database import Base, engine
from bot.src.models.user import User
from bot.src.models.establishment import Establishment
from bot.src.models.establishment_type import EstablishmentType

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
