from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base
import enum

class MatchStatus(str, enum.Enum):
    setup = "setup"
    live = "live"
    expired = "expired"
    archived = "archived"

class TeamSide(str, enum.Enum):
    home = "home"
    away = "away"

class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(64), unique=True, index=True)
    coach_token = Column(String) # For simple auth if needed
    match_status = Column(Enum(MatchStatus), default=MatchStatus.setup, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, index=True)
    version = Column(Integer, default=0)
    deleted_at = Column(DateTime, nullable=True) # Soft delete

    teams = relationship("Team", back_populates="room", cascade="all, delete-orphan")
    snapshots = relationship("Snapshot", back_populates="room", cascade="all, delete-orphan")

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String, ForeignKey("rooms.room_id", ondelete="CASCADE"), nullable=False)
    name = Column(String)
    color = Column(String)
    side = Column(Enum(TeamSide), nullable=False)

    room = relationship("Room", back_populates="teams")
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")

class Player(Base):
    __tablename__ = "players"

    player_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)
    # Also linking to room might be redundant if we go through team, but specs said room_id FK. 
    # Keeping it simple with team link for now unless optimal query patterns suggest otherwise.
    # Spec: player has room_id FK. I'll add it for compliance.
    room_id = Column(String, ForeignKey("rooms.room_id", ondelete="CASCADE"), nullable=False)
    
    x = Column(Float) # Check 0-1 enforced in app logic
    y = Column(Float) # Check 0-1 enforced in app logic
    label = Column(String)
    role = Column(String) # GK, DEF, etc.
    is_goalkeeper = Column(Boolean, default=False)

    team = relationship("Team", back_populates="players")
    # room relationship could be added but might cause double linkage issues if not careful.

class Snapshot(Base):
    __tablename__ = "snapshots"

    snapshot_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String, ForeignKey("rooms.room_id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer)
    full_state = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("Room", back_populates="snapshots")
