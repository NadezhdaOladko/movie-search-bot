from datetime import datetime

from sqlalchemy import create_engine, DateTime, insert
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
    search_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


def save_movie_to_history(user_id: int, movie: dict) -> None:
    """Сохраняет запись о фильме в базе данных."""
    with Session() as session:
        session.execute(
            insert(Movie).values(
                user_id=user_id,
                movie_title=movie["title"],
                search_date=datetime.now()
            )
        )
        session.commit()
