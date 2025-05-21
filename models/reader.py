from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(
        back_populates="reader", cascade="all, delete-orphan"
    )
