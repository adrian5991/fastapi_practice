from sqlalchemy.orm import Session

from . import models, schemas


def get_player_by_id(db: Session, player_id: int):
    return db.get(models.Player, player_id)


def get_players(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Player)
        .order_by(models.Player.last_name)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_player(db: Session, player: schemas.PlayerModel):
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def delete_player(db: Session, player_id: int):
    pass


def update_player(db: Session, player_id: int):
    pass
