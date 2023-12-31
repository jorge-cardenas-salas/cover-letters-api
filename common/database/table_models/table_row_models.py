from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from common.database.database import Base


class UserTableRow(Base):
    __tablename__ = "tblUser"
    # __table_args__ = {"schema": "coverletter"} # Used only for SQL Server

    """
    SQLAlchemy ORM (Object Relational Model) representation of the table
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    # relationship() can be backtraced, but keeping it simple for this example
    skills: Mapped[List["SkillTableRow"]] = relationship()


class SkillTableRow(Base):
    __tablename__ = "tblSkill"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    level: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column("userId", ForeignKey("tblUser.id"))
