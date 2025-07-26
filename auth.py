import secrets
import uuid
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from database import get_sessions_collection
from external_api import external_api
from models import UserResponse, GameSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

def generate_session_token() -> str:
    """Generate a secure session token for game authentication"""
    return secrets.token_urlsafe(32)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user_from_token(token: str) -> Optional[UserResponse]:
    """Get current user info from JWT token via external API"""
    user = await external_api.get_user_me(token)
    return user

async def get_current_user_from_cookie(jwt_token: Optional[str] = Cookie(None)) -> UserResponse:
    """Get current user from JWT cookie"""
    if not jwt_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chưa xác thực"
        )
    
    user = await get_current_user_from_token(jwt_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin xác thực không hợp lệ"
        )
    return user

async def get_current_user_from_header(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> UserResponse:
    """Get current user from Authorization header"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chưa xác thực"
        )
    
    user = await get_current_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin xác thực không hợp lệ"
        )
    return user

async def create_game_session(user: UserResponse, station_id: str) -> str:
    """Create a game session and return session token"""
    session_token = generate_session_token()
    session = GameSession(
        user_id=user.id or user.username,
        username=user.username,
        team_name=user.team_name,
        station_id=station_id,
        session_token=session_token,
        created_at=datetime.utcnow(),
        is_active=True
    )
    
    sessions_collection = get_sessions_collection()
    await sessions_collection.insert_one(session.dict())
    
    return session_token

async def verify_game_session(session_token: str, station_id: str) -> Optional[GameSession]:
    """Verify game session token"""
    sessions_collection = get_sessions_collection()
    session_data = await sessions_collection.find_one({
        "session_token": session_token,
        "station_id": station_id,
        "is_active": True
    })
    
    if session_data:
        return GameSession(**session_data)
    return None

async def find_active_session(user: UserResponse, station_id: str) -> Optional[GameSession]:
    """Find an active session for a user and station"""
    sessions_collection = get_sessions_collection()
    session_data = await sessions_collection.find_one({
        "username": user.username,
        "station_id": station_id,
        "is_active": True
    })
    
    if session_data:
        return GameSession(**session_data)
    return None

async def invalidate_game_session(session_token: str):
    """Invalidate game session after game completion"""
    sessions_collection = get_sessions_collection()
    await sessions_collection.update_one(
        {"session_token": session_token},
        {"$set": {"is_active": False}}
    )
