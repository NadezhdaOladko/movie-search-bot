from datetime import datetime

from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


engine = create_engine('sqlite:///movies.db')
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = 'movie_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    movie_title: Mapped[str] = mapped_column(nullable=False)
    ssearch_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
