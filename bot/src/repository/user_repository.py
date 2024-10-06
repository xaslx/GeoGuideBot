from bot.src.repository.sqlalchemy_repository import SQLAlchemyRepository
from bot.src.models.user import User



class UserRepository(SQLAlchemyRepository):

    model: User = User