from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = "users"  # Имя таблицы
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)