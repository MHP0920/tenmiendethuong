import os
from dotenv import load_dotenv

load_dotenv(".env")

class Settings:
    # MongoDB Configuration
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "game_login_system")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # External API Configuration
    AUTH_API_BASE_URL: str = os.getenv("AUTH_API_BASE_URL", "http://localhost:5000")
    STATION_API_BASE_URL: str = os.getenv("STATION_API_BASE_URL", "http://localhost:5000")
    
    # Skip PIN Configuration
    SKIP_PIN: str = os.getenv("SKIP_PIN", "1234")
    
    # Game PIN Configuration (only for Domain Game)
    TEN_MIEN_DE_THUONG_PIN: str = os.getenv("TEN_MIEN_DE_THUONG_PIN")

    # FastAPI Configuration
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()
print("PIN loaded from environment variable:")
print(f"TEN_MIEN_DE_THUONG_PIN: {settings.TEN_MIEN_DE_THUONG_PIN}")
