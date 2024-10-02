from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey



class Establishment(Base):
    __tablename__ = 'establishments'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    address: Mapped[str]
    type_id: Mapped[int] = mapped_column(ForeignKey('establishment_types.id'))




