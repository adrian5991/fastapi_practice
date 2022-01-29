from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


# create models in database
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Independent session per request; yielded value is injected into path operation
# once response is delivered, everything after yield is executed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Player: API"}


@app.get("/players/{player_id}", response_model=schemas.PlayerModel)
def get_player_by_id(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player_by_id(db, player_id)
    if player is None:
        raise HTTPException(404, detail="Player not found")
    return player


@app.get("/players", response_model=List[schemas.PlayerModel])
def get_players(db: Session = Depends(get_db)):
    players = crud.get_players(db)
    return players


@app.post("/players", status_code=201, response_model=schemas.PlayerModel)
def create_player(player: schemas.PlayerModel, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)


@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player_by_id(db, player_id)
    if player is None:
        raise HTTPException(404, detail="Player not found")
    return crud.delete_player(db, player)
