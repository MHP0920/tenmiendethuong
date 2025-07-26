import httpx
from typing import Optional, Dict, Any
from config import settings
from models import TokenResponse, UserResponse, CanVisitResponse, VisitPriceResponse

class StationInfo:
    def __init__(self, station_id: str, name: str, codename: str, difficulty: str, station_group: Dict[str, Any]):
        self.station_id = station_id
        self.name = name
        self.codename = codename
        self.difficulty = difficulty
        self.station_group = station_group

class ExternalAPIClient:
    def __init__(self):
        self.auth_base_url = settings.AUTH_API_BASE_URL
        self.station_base_url = settings.STATION_API_BASE_URL
    
    async def sign_in(self, username: str, password: str) -> Optional[TokenResponse]:
        """Call external auth API to sign in user"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.auth_base_url}/api/auth/sign-in",
                    json={"username": username, "password": password},
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200 or response.status_code == 201:
                    data = response.json()
                    return TokenResponse(accessToken=data["accessToken"])
                return None
            except Exception as e:
                print(f"Error during sign in: {e}")
                return None
    
    async def get_user_me(self, token: str) -> Optional[UserResponse]:
        """Validate JWT token and get user info"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.auth_base_url}/api/team/my-team",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                print(f"Response status code: {response.status_code}, {response.text}")
                if response.status_code == 200 or response.status_code == 201:
                    data = response.json()
                    return UserResponse(
                        username=data["username"], 
                        team_name=data.get("name"),  # Extract team name from the response
                        id=data.get("id"),
                        team_id=data.get("_id"),  # Assuming the team ID is in "_id" field
                        coins=data.get("coins"),
                        unlocked_puzzles=data.get("unlockedPuzzles", []),
                        skill_cards=data.get("skillCards", [])
                    )
                return None
            except Exception as e:
                print(f"Error getting user info: {e}")
                return None
    
    async def get_station_by_codename(self, codename: str, token: str) -> Optional[StationInfo]:
        """Get station information by codename"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.station_base_url}/api/station/codename/{codename}",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                print(f"Station info response: {response.status_code}, {response.text}")
                if response.status_code == 200:
                    data = response.json()
                    return StationInfo(
                        station_id=data["_id"],
                        name=data["name"],
                        codename=data["codename"],
                        difficulty=data["difficulty"],
                        station_group=data["stationGroup"]
                    )
                return None
            except Exception as e:
                print(f"Error getting station info: {e}")
                return None

    async def get_station_by_id(self, station_id: str, token: str) -> Optional[StationInfo]:
        """Get station information by station ID"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.station_base_url}/api/station/id/{station_id}",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                print(f"Station info by ID response: {response.status_code}, {response.text}")
                if response.status_code == 200:
                    data = response.json()
                    return StationInfo(
                        station_id=data["_id"],
                        name=data["name"],
                        codename=data["codename"],
                        difficulty=data["difficulty"],
                        station_group=data["stationGroup"]
                    )
                return None
            except Exception as e:
                print(f"Error getting station info by ID: {e}")
                return None
    
    async def can_visit_station(self, station_codename: str, token: str) -> Optional[CanVisitResponse]:
        """Check if user can visit the station by codename"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.station_base_url}/api/station/can-visit/{station_codename}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200 and response.text == 'true':
                    return CanVisitResponse(reason="nothing")
                else:
                    data = response.json()
                    return CanVisitResponse(reason=str(data["error"]).lower())
            except Exception as e:
                print(f"Error checking can visit: {e}")
                return None
    

    
    async def get_visit_price(self, station_codename: str, token: str) -> Optional[VisitPriceResponse]:
        """Get the price for visiting a station by codename"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.station_base_url}/api/station/visit-price/{station_codename}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    return VisitPriceResponse(
                        price=response.text, 
                        currency="Bytes"  # Assuming currency is in Bytes for the game
                    )
                return None
            except Exception as e:
                print(f"Error getting visit price: {e}")
                return None
    
    async def visit_station(self, station_codename: str, pin: str, team_username: str) -> bool:
        """Pay for visiting a station using codename and PIN"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.station_base_url}/api/station/visit?teamUsername={team_username}",
                    json={
                        "stationCodename": station_codename,
                        "pin": pin
                    },
                    headers={"Content-Type": "application/json"}
                )
                print(pin)
                print(f"Visit station response: {response.status_code}, {response.text}")
                return response.status_code == 200 or response.status_code == 201
            except Exception as e:
                print(f"Error during station visit payment: {e}")
                return False
    
    async def skip_station(self, station_codename: str, pin: str, team_id: str) -> bool:
        """Skip a station with PIN and teamId"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.station_base_url}/api/station/skip?teamId={team_id}",
                    json={
                        "stationCodename": station_codename,
                        "pin": pin
                    },
                    headers={
                        "Content-Type": "application/json"
                    }
                )
                print(f"Skip station response: {response.status_code}, {response.text}")
                print(pin)
                return response.status_code == 200 or response.status_code == 201
            except Exception as e:
                print(f"Error during station skip: {e}")
                return False

    async def unskip_station(self, station_codename: str, pin: str, team_id: str) -> bool:
        """Unskip a station (pay to remove from skipped list) with PIN and teamId"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.station_base_url}/api/station/unskip?teamId={team_id}&noCoinsUpdate=false",
                    json={
                        "stationCodename": station_codename,
                        "pin": pin
                    },
                    headers={
                        "Content-Type": "application/json"
                    }
                )
                print(f"Unskip station response: {response.status_code}, {response.text}")
                return response.status_code == 200 or response.status_code == 201
            except Exception as e:
                print(f"Error during station unskip: {e}")
                return False

    async def unlock_puzzle(self, station_codename: str, pin: str, team_username: str) -> bool:
        """Unlock a puzzle after successful completion"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.auth_base_url}/api/team/unlock-puzzle?teamUsername={team_username}",
                    json={
                        "stationCodename": station_codename,
                        "pin": pin
                    },
                    headers={
                        "Content-Type": "application/json"
                    }
                )
                print(f"Unlock puzzle response: {response.status_code}, {response.text}")
                return response.status_code == 200 or response.status_code == 201
            except Exception as e:
                print(f"Error during puzzle unlock: {e}")
                return False

# Create a global instance
external_api = ExternalAPIClient()
