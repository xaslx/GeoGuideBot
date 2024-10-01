from bot.src.repository.sqlalchemy_repositroy import SQLAlchemyRepository
from bot.src.models.establishment import Establishment



class EstablishmentRepository(SQLAlchemyRepository):

    model: Establishment = Establishment