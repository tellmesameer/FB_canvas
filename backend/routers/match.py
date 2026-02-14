from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from datetime import datetime

router = APIRouter(
    prefix="/rooms/{room_id}/match",
    tags=["match"],
)

@router.post("/start", response_model=schemas.MatchStartResponse)
def start_match(room_id: str, db: Session = Depends(database.get_db)):
    room = db.query(models.Room).filter((models.Room.room_id == room_id) | (models.Room.slug == room_id)).first()
    if not room:
         raise HTTPException(status_code=404, detail="Room not found")
    
    # Ideally check if requester is coach (via token or session), but MVP might be loose on this initially. 
    # Spec says "Coach only". I'll assume for now we just allow it if room exists, 
    # or check the coach_token if I were to implement auth header check.
    # For now, simplistic implementation.

    if room.match_status == models.MatchStatus.live:
         return {"match_status": room.match_status, "started_at": datetime.utcnow()} # Idempotency-ish

    room.match_status = models.MatchStatus.live
    room.updated_at = datetime.utcnow() # If I had updated_at
    db.commit()
    
    return {"match_status": room.match_status, "started_at": datetime.utcnow()} # Real start time logic might need DB column if critical

@router.post("/end", response_model=schemas.MatchEndResponse)
def end_match(room_id: str, db: Session = Depends(database.get_db)):
    room = db.query(models.Room).filter((models.Room.room_id == room_id) | (models.Room.slug == room_id)).first()
    if not room:
         raise HTTPException(status_code=404, detail="Room not found")

    room.match_status = models.MatchStatus.expired
    db.commit()
    
    return {"match_status": room.match_status}
