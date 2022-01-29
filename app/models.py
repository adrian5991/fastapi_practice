from sqlalchemy import Column, Integer, String

from .database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)
    jersey_number = Column(Integer)
