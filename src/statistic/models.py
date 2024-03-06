from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class Statistic(Base):
    __tablename__ = 'statistic_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    views: Mapped[int] = mapped_column(nullable=True)
    clicks: Mapped[int] = mapped_column(nullable=True)
    cost: Mapped[float] = mapped_column(nullable=True)
