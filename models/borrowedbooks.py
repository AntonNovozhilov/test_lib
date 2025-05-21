from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.book import Book
from models.reader import Reader


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey(Reader.id), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey(Book.id), nullable=False)
    borrowed_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now()
    )
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)
    reader: Mapped["Reader"] = relationship(back_populates="borrowed_books")
    book: Mapped["Book"] = relationship(back_populates="borrowed_books")
