from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import uuid
import enum

# Enums (Duplicate of models for Pydantic use, or import if shared properly)
# Given simple setup, redefining here is often cleaner for strict separation of concerns (API vs DB)

class MatchStatus(str, enum.Enum):
    setup = "setup"
    live = "live"
    expired = "expired"
    archived = "archived"

class TeamSide(str, enum.Enum):
    home = "home"
    away = "away"

# --- Models ---

class PlayerBase(BaseModel):
    x: float = Field(..., ge=0, le=1)
    y: float = Field(..., ge=0, le=1)
    label: Optional[str] = None
    role: Optional[str] = None
    is_goalkeeper: bool = False

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class Player(PlayerBase):
    player_id: str
    team_id: str
    room_id: str

    class Config:
        from_attributes = True

class TeamBase(BaseModel):
    name: str = Field(..., max_length=50)
    color: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$")

class TeamUpdate(TeamBase):
    pass

class Team(TeamBase):
    team_id: str
    room_id: str
    side: TeamSide
    players: List[Player] = []

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    pass

class RoomCreate(BaseModel):
    room_name: Optional[str] = None # Not used in DB but maybe for UI logic? Spec says "room_name" in request.
    match_duration_minutes: int = Field(90, gt=0, le=300)
    custom_slug: Optional[str] = None

class Room(BaseModel):
    room_id: str
    slug: str
    match_status: MatchStatus
    created_at: datetime
    expires_at: Optional[datetime]
    version: int
    teams: List[Team] = []

    class Config:
        from_attributes = True

class RoomResponse(BaseModel):
    data: Room
    meta: Optional[dict] = None

class TeamResponse(BaseModel):
    data: Team
    meta: Optional[dict] = None

class TeamListResponse(BaseModel):
    data: List[Team]
    meta: Optional[dict] = None

# --- Match Control ---

class MatchStartResponse(BaseModel):
    match_status: MatchStatus
    started_at: datetime

class MatchEndResponse(BaseModel):
    match_status: MatchStatus

# --- Generic Response Wrappers ---
# Can be used to strictly typing responses
