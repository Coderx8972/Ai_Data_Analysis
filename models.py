from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime, UTC

# Base class for models
class Base(DeclarativeBase):  # to make a entirely new catalog
    pass

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50),nullable=False)
    email: Mapped[str] = mapped_column(String(50))
    phone_number:Mapped[str] = mapped_column(String(10))

class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50),nullable=False)
    author: Mapped[str] = mapped_column(String(50),nullable=False)
    total_books: Mapped[int] = mapped_column(nullable=False)
    available_books:Mapped[int] = mapped_column()

class Transaction(Base):
    __tablename__= "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id : Mapped[int] = mapped_column(ForeignKey("students.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrow_date: Mapped[datetime] = mapped_column(default=lambda:datetime.now(UTC))
    return_date: Mapped[datetime] = mapped_column(nullable=True)
