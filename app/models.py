from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    index = Column(Integer)
    name_fa = Column(String(255))
    name_en = Column(String(255))
    website = Column(Text)
    website_desc = Column(Text)
    magazine_desc = Column(Text)
    file_number = Column(Integer)  # Like 20251201
    sector = Column(String(255))
    country = Column(String(255))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    role = Column(String(50))