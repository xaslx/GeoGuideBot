from bot.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class EstablishmentType(Base):
    __tablename__ = 'establishment_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(unique=True)