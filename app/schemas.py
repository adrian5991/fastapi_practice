from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Positions(str, Enum):
    pg = "PG"
    sg = "SG"
    sf = "SF"
    pf = "PF"
    c = "C"


class PlayerModel(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    position: Positions
    jersey_number: int

    class Config:
        orm_mode = True
