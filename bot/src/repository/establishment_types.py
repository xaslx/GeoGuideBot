from bot.src.repository.sqlalchemy_repositroy import SQLAlchemyRepository
from bot.src.models.establishment_type import EstablishmentType



class EstablishmentTypeRepository(SQLAlchemyRepository):

    model: EstablishmentType = EstablishmentType