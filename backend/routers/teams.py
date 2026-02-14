from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from datetime import datetime

router = APIRouter(
    prefix="/rooms/{room_id}/teams",
    tags=["teams"],
)

@router.get("/", response_model=schemas.TeamListResponse)
def get_teams(room_id: str, db: Session = Depends(database.get_db)):
    # Verify room exists
    room = db.query(models.Room).filter((models.Room.room_id == room_id) | (models.Room.slug == room_id)).first()
    if not room:
         raise HTTPException(status_code=404, detail="Room not found")
    
    # Use the resolved room_id in case slug was passed
    teams = db.query(models.Team).filter(models.Team.room_id == room.room_id).all()
    return {"data": teams, "meta": {"timestamp": datetime.utcnow()}}

@router.put("/{team_id}", response_model=schemas.TeamResponse)
def update_team(room_id: str, team_id: str, team_update: schemas.TeamUpdate, db: Session = Depends(database.get_db)):
    # Verify room and team
    room = db.query(models.Room).filter((models.Room.room_id == room_id) | (models.Room.slug == room_id)).first()
    if not room:
         raise HTTPException(status_code=404, detail="Room not found")
    
    team = db.query(models.Team).filter(models.Team.team_id == team_id, models.Team.room_id == room.room_id).first()
    if not team:
         # Try finding by side ("home" or "away")? 
         # Spec says team_id is "home" or "away" in example, but schema says UUID. 
         # Let's support verifying if they used side as ID for convenience, or just stick to ID.
         # Spec example: "team_id": "home".
         # My models.py uses UUID default. 
         # Wait, spec says: "team_id": "home" in example JSON.
         # But constraints say: "team_id": UUID PRIMARY KEY.
         # Conflict in spec? 
         # "3.1 Get Teams" example shows "team_id": "home". 
         # "3.2 Teams Table" says "team_id": UUID.
         # I will stick to UUID for actual ID, but maybe I should have initialized them with known IDs if I wanted "home"/"away".
         # For now, stick to finding by actual team_id.
        raise HTTPException(status_code=404, detail="Team not found")

    # Business Rule: Lock if match has started
    if room.match_status != models.MatchStatus.setup:
        raise HTTPException(status_code=400, detail="Cannot edit team after match start")

    team.name = team_update.name
    team.color = team_update.color
    db.commit()
    db.refresh(team)

    return {"data": team, "meta": {"timestamp": datetime.utcnow()}}
