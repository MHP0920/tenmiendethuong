from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    accessToken: str

class UserResponse(BaseModel):
    username: str
    team_name: Optional[str] = None
    id: Optional[str] = None
    team_id: Optional[str] = None
    coins: Optional[int] = None
    unlocked_puzzles: Optional[List[Dict[str, Any]]] = None
    skill_cards: Optional[List[Dict[str, Any]]] = None

class CanVisitResponse(BaseModel):
    reason: str  # "skip", "nothing", "not yet"

class GameSession(BaseModel):
    user_id: str
    username: str
    team_name: Optional[str] = None
    station_id: str
    session_token: str
    created_at: datetime
    is_active: bool = True

class PaymentRequest(BaseModel):
    station_id: str
    amount: Optional[float] = None

class VisitPriceResponse(BaseModel):
    price: float
    currency: str = "Byte"
