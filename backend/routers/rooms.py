from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

@router.post("/", response_model=schemas.RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: schemas.RoomCreate, db: Session = Depends(database.get_db)):
    # Check if slug exists if provided
    if room.custom_slug:
        existing_room = db.query(models.Room).filter(models.Room.slug == room.custom_slug).first()
        if existing_room:
             raise HTTPException(status_code=400, detail="Slug already exists")
        slug = room.custom_slug
    else:
        # Generate simple unique slug or use UUID
        # For now, using uuid as slug if not provided, or could be random string
        slug = str(uuid.uuid4())

    new_room = models.Room(
        room_id=str(uuid.uuid4()),
        slug=slug,
        match_status=models.MatchStatus.setup,
        coach_token=str(uuid.uuid4()) # generated coach token
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    
    # Initialize Teams (Home/Away)
    home_team = models.Team(
        team_id=str(uuid.uuid4()),
        room_id=new_room.room_id,
        name="Home",
        color="#0055ff", # Default Blue
        side=models.TeamSide.home
    )
    away_team = models.Team(
        team_id=str(uuid.uuid4()),
        room_id=new_room.room_id,
        name="Away",
        color="#ff0000", # Default Red
        side=models.TeamSide.away
    )
    db.add(home_team)
    db.add(away_team)
    db.commit()

    # Initialize Players (11 per team)
    players = []
    # Home Team (Blue)
    for i in range(11):
        is_gk = (i == 0)
        # Simple formation: GK at 0.1, others distributed
        x = 0.1 if is_gk else 0.3 + (i // 4) * 0.15
        y = 0.5 if is_gk else 0.1 + (i % 4) * 0.25
        
        players.append(models.Player(
            player_id=str(uuid.uuid4()),
            team_id=home_team.team_id,
            room_id=new_room.room_id,
            x=x,
            y=y,
            label=str(i + 1),
            role="GK" if is_gk else "Player",
            is_goalkeeper=is_gk
        ))

    # Away Team (Red)
    for i in range(11):
        is_gk = (i == 0)
        # Mirror positions
        x = 0.9 if is_gk else 0.7 - (i // 4) * 0.15
        y = 0.5 if is_gk else 0.1 + (i % 4) * 0.25
        
        players.append(models.Player(
            player_id=str(uuid.uuid4()),
            team_id=away_team.team_id,
            room_id=new_room.room_id,
            x=x,
            y=y,
            label=str(i + 1),
            role="GK" if is_gk else "Player",
            is_goalkeeper=is_gk
        ))

    db.add_all(players)
    db.commit()
    
    # Refresh room to load relationships (teams)
    db.refresh(new_room)

    return {"data": new_room, "meta": {"request_id": str(uuid.uuid4()), "timestamp": datetime.utcnow()}}

@router.get("/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: str, db: Session = Depends(database.get_db)):
    # Try finding by room_id or slug
    room = db.query(models.Room).filter((models.Room.room_id == room_id) | (models.Room.slug == room_id)).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Check if soft deleted? Spec says soft delete. 
    if room.deleted_at:
         raise HTTPException(status_code=404, detail="Room not found")

    return {"data": room, "meta": {"timestamp": datetime.utcnow()}}

@router.delete("/{room_id}", status_code=status.HTTP_200_OK)
def delete_room(room_id: str, db: Session = Depends(database.get_db)):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"data": {"deleted": True, "scheduled_purge_at": "ISO-7-days-later"}}
