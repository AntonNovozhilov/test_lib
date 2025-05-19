from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.base import Base
from models.reader import Reader
from models.book import Book


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey(Reader.id), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey(Book.id), nullable=False)
    borrowed_date: Mapped[str] = mapped_column(nullable=False)
    return_date: Mapped[str] = mapped_column(nullable=True)
