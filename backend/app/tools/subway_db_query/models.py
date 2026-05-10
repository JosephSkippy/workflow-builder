from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Train(Base):
    __tablename__ = "train"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(String)
    day: Mapped[str] = mapped_column(String)
    station: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String)
    min_delay: Mapped[int] = mapped_column(Integer)
    min_gap: Mapped[int] = mapped_column(Integer)
    bound: Mapped[str] = mapped_column(String)
    line: Mapped[str] = mapped_column(String)
    vehicle: Mapped[str] = mapped_column(String)
