from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=True)
    isbn: Mapped[str] = mapped_column(nullable=True, unique=True)
    count: Mapped[int] = mapped_column(nullable=True, default=1)
    description: Mapped[str] = mapped_column(nullable=True)
    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )
