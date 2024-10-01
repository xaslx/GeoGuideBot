from bot.src.repository.sqlalchemy_repositroy import SQLAlchemyRepository
from bot.src.models.user import User



class UserRepository(SQLAlchemyRepository):

    model: User = User