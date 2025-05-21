from sqlalchemy import Column, Integer, String
from src.database import Base


class User(Base):
    """
    Model for storing users in db
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    residing_place = Column(String,nullable=False)
    photo_url = Column(String, nullable=False)

