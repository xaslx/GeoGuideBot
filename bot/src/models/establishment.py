from database import Base
from sqlalchemy.orm import Mapped, mapped_column



class Establishment(Base):
    __tablename__ = 'establishments'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    address: Mapped[str]
    photo_url: Mapped[str]




