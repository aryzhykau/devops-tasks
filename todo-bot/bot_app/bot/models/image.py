from sqlalchemy import Column, Integer, String
from bot_app import Base


class User(Base):
    __tablename__ = "images"  # Имя таблицы
    id = Column(Integer, primary_key=True, autoincrement=True)
    s3_link = Column(String(100), nullable=True)
    s3_path = Column(String(100), nullable=True)