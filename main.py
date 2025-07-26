from fastapi import FastAPI, Request, HTTPException, status, Depends, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from datetime import timedelta

from config import settings
from database import connect_to_mongo, close_mongo_connection
from models import LoginRequest, UserResponse, GameSession
from auth import (
    get_current_user_from_cookie, 
    get_current_user_from_header,
    create_game_session,
    verify_game_session,
    invalidate_game_session,
    find_active_session
)
from external_api import external_api
from domain_data import get_random_domains, verify_answers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Game Login System",
    description="Unified login system for multiple games",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler for authentication errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        # For HTML requests, redirect to login page
        accept_header = request.headers.get("accept", "")
        if "text/html" in accept_header:
            return RedirectResponse(url="/login", status_code=302)
    
    # For API requests or other errors, return JSON
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Templates
templates = Jinja2Templates(directory="templates")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint - redirect to games if authenticated, otherwise to login"""
    try:
        # Try to get user from cookie
        jwt_token = request.cookies.get("jwt_token")
        if jwt_token:
            user = await external_api.get_user_me(jwt_token)
            if user:
                return RedirectResponse(url="/games", status_code=302)
    except:
        pass
    
    return RedirectResponse(url="/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, station_id: str = None, redirect: str = None):
    """Display login page"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "station_id": station_id,
        "redirect": redirect
    })

@app.post("/login")
async def login(request: LoginRequest, response: Response):
    """Handle login request"""
    # Call external auth API
    token_response = await external_api.sign_in(request.username, request.password)
    
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không hợp lệ"
        )
    
    # Set JWT token as httpOnly cookie
    response.set_cookie(
        key="jwt_token",
        value=token_response.accessToken,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return {"message": "Đăng nhập thành công"}

@app.post("/logout")
async def logout(response: Response):
    """Handle logout request"""
    response.delete_cookie(key="jwt_token")
    return {"message": "Đăng xuất thành công"}

@app.get("/api/game/ten-mien-de-thuong/domains")
async def get_game_domains(current_user: UserResponse = Depends(get_current_user_from_cookie)):
    """Get random domains for the domain classification game"""
    domains = get_random_domains(30)
    
    # Return domains without revealing correct answers
    return {
        "domains": [{"domain": item["domain"]} for item in domains],
        "total_count": len(domains),
        "target_score": 21,  # Need more than 20 correct to pass
        "instructions": "Phân loại các tên miền sau đây thành 'Hợp pháp' hoặc 'Lừa đảo'. Bạn cần phân loại đúng trên 20/30 tên miền để hoàn thành thử thách."
    }

@app.post("/api/game/ten-mien-de-thuong/verify")
async def verify_domain_classification(
    request: Request,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Verify domain classification answers"""
    data = await request.json()
    user_answers = data.get("answers", [])
    
    if not user_answers:
        raise HTTPException(status_code=400, detail="Không có đáp án nào được gửi")
    
    # Get the same random domains (we need to store this per session in real implementation)
    # For now, we'll validate against the submitted domains
    domains_to_verify = []
    for answer in user_answers:
        domain = answer.get("domain")
        user_classification = answer.get("is_legitimate")
        
        if not domain:
            continue
            
        # Check if domain is in our lists
        from domain_data import LEGITIMATE_DOMAINS, SUSPICIOUS_DOMAINS
        
        if domain in LEGITIMATE_DOMAINS:
            correct_classification = True
        elif domain in SUSPICIOUS_DOMAINS:
            correct_classification = False
        else:
            # Unknown domain, skip
            continue
            
        domains_to_verify.append({
            "domain": domain,
            "is_legitimate": correct_classification
        })
    
    # Verify answers
    result = verify_answers(user_answers, domains_to_verify)
    
    return {
        "correct_count": result["correct_count"],
        "total_count": result["total_count"],
        "accuracy": result["accuracy"],
        "passed": result["passed"],
        "message": f"Bạn đã phân loại đúng {result['correct_count']}/{result['total_count']} tên miền. " +
                  ("Chúc mừng! Bạn đã vượt qua thử thách!" if result["passed"] else "Cần phân loại đúng trên 20 tên miền để pass.")
    }

@app.get("/user/profile")
async def get_user_profile(current_user: UserResponse = Depends(get_current_user_from_cookie)):
    """Get current user profile"""
    return current_user

@app.get("/games", response_class=HTMLResponse)
async def games_page(request: Request, current_user: UserResponse = Depends(get_current_user_from_cookie)):
    """Display games selection page"""
    return templates.TemplateResponse("games.html", {"request": request})

@app.get("/game-flow/{codename}")
async def game_flow(
    codename: str,
    request: Request,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Handle game flow - check eligibility and redirect accordingly"""
    # Get JWT token from cookie for external API calls
    jwt_token = request.cookies.get("jwt_token")
    
    # First, get station information by codename
    station_info = await external_api.get_station_by_codename(codename, jwt_token)
    
    if not station_info:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy trạm với mã '{codename}'")
    
    station_id = station_info.station_id
    
    # Always check if user can visit the station first (eligibility check)
    # This must be checked even if user has existing sessions
    can_visit = await external_api.can_visit_station(codename, jwt_token)
    
    if not can_visit:
        raise HTTPException(status_code=500, detail="Không thể kiểm tra tình trạng truy cập trạm")
    
    # Check if puzzle is already unlocked by getting team info
    team_info = await external_api.get_user_me(jwt_token)
    if team_info and team_info.unlocked_puzzles:
        # Check if this station is already unlocked
        for puzzle in team_info.unlocked_puzzles:
            if puzzle.get('_id') == station_id or puzzle.get('codename') == codename:
                # Puzzle already unlocked - show completion page and auto-logout
                return templates.TemplateResponse("puzzle_completed.html", {
                    "request": request,
                    "station_name": station_info.name,
                    "codename": codename,
                    "station_id": station_id
                })
    
    if can_visit.reason == "not yet":
        # User is not eligible yet - show user-friendly error page
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_type": "not_yet",
            "status_code": 403,
            "error_detail": "Bạn chưa đủ điều kiện để truy cập trạm này",
            "station_name": station_info.name,
            "codename": codename,
            "station_id": station_id
        })
    elif can_visit.reason == "conflict":
        # Team has skipped this station and must pay to unskip - show user-friendly error page
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_type": "conflict", 
            "status_code": 409,
            "error_detail": "Đội đã bỏ qua trạm này và không thể truy cập lại cho đến khi hủy bỏ qua (trả phí)",
            "station_name": station_info.name,
            "codename": codename,
            "station_id": station_id
        })
    
    # Only check for existing sessions if user is eligible
    # This ensures users cannot bypass eligibility with old sessions
    existing_session = await find_active_session(current_user, station_id)
    if existing_session:
        # Even with existing session, user must still be eligible
        # Redirect to game with existing session token using the original codename
        return RedirectResponse(url=f"/game/{codename}?session_token={existing_session.session_token}", status_code=302)
    
    # No active session, proceed based on eligibility reason
    if can_visit.reason == "skip":
        # User needs to pay for skipped game
        return RedirectResponse(
            url=f"/payment?station_id={station_id}&codename={codename}&type=skip", 
            status_code=302
        )
    elif can_visit.reason == "nothing":
        # User can proceed to payment page
        return RedirectResponse(
            url=f"/payment?station_id={station_id}&codename={codename}&type=visit", 
            status_code=302
        )
    else:
        raise HTTPException(status_code=400, detail="Tình trạng tư cách không xác định")

@app.get("/payment", response_class=HTMLResponse)
async def payment_page(request: Request, station_id: str, codename: str, type: str, current_user: UserResponse = Depends(get_current_user_from_cookie)):
    """Display payment page"""
    # Get JWT token and station info to display game name
    jwt_token = request.cookies.get("jwt_token")
    station_info = await external_api.get_station_by_codename(codename, jwt_token)
    
    station_name = station_info.name if station_info else codename
    
    return templates.TemplateResponse("payment.html", {
        "request": request,
        "station_id": station_id,
        "codename": codename,
        "payment_type": type,
        "station_name": station_name
    })

@app.get("/game-flow/{station_id}/price")
async def get_visit_price(
    station_id: str,
    request: Request,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Get the price for visiting a station"""
    jwt_token = request.cookies.get("jwt_token")
    
    # Get station info to get codename
    station_info = await external_api.get_station_by_id(station_id, jwt_token)
    if not station_info:
        raise HTTPException(status_code=404, detail="Không tìm thấy trạm")
    
    price_info = await external_api.get_visit_price(station_info.codename, jwt_token)
    
    if not price_info:
        raise HTTPException(status_code=500, detail="Không thể lấy thông tin giá truy cập")
    
    return price_info

@app.post("/game-flow/{station_id}/pay-visit")
async def pay_visit(
    station_id: str,
    request: Request,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Pay for visiting a station"""
    # Check if user has username
    if not current_user.username:
        raise HTTPException(status_code=400, detail="Không tìm thấy tên đội của người dùng")
    
    # Get JWT token and station info to find the codename
    jwt_token = request.cookies.get("jwt_token")
    station_info = await external_api.get_station_by_id(station_id, jwt_token)
    
    if not station_info:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy trạm với ID '{station_id}'")
    
    # Get the appropriate PIN for this game
    pin = get_game_pin(station_info.codename)
    if not pin:
        raise HTTPException(status_code=400, detail="Mã game không hợp lệ")
    
    payment_success = await external_api.visit_station(station_info.codename, pin, current_user.username)
    
    if not payment_success:
        raise HTTPException(status_code=500, detail="Thanh toán thất bại")
    
    # Create game session and generate session token
    session_token = await create_game_session(current_user, station_id)
    
    return {
        "message": "Thanh toán truy cập thành công",
        "session_token": session_token
    }

@app.post("/game-flow/{station_id}/unskip")
async def unskip_station_endpoint(
    station_id: str,
    request: Request,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Unskip a station (automatically pays for removal from skipped list)"""
    # Check if user has username
    if not current_user.username:
        raise HTTPException(status_code=400, detail="Không tìm thấy tên đội của người dùng")
    
    # Get JWT token and station info to find the codename
    jwt_token = request.cookies.get("jwt_token")
    station_info = await external_api.get_station_by_id(station_id, jwt_token)
    
    if not station_info:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy trạm với ID '{station_id}'")
    
    # Get the appropriate PIN for this game
    pin = get_game_pin(station_info.codename)
    if not pin:
        raise HTTPException(status_code=400, detail="Mã game không hợp lệ")
    
    # Use unskip API which automatically pays for removing from skipped list
    unskip_success = await external_api.unskip_station(station_info.codename, pin, current_user.team_id)
    
    if not unskip_success:
        raise HTTPException(status_code=500, detail="Hủy bỏ qua thất bại")
    
    return {"message": "Hủy bỏ qua thành công"}

@app.get("/game/{codename}", response_class=HTMLResponse)
async def game_page(
    request: Request,
    codename: str,
    session_token: str = None,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Display game page"""
    if not session_token:
        raise HTTPException(status_code=400, detail="Cần có session token")
    
    # Get JWT token and station info
    jwt_token = request.cookies.get("jwt_token")
    station_info = await external_api.get_station_by_codename(codename, jwt_token)
    
    if not station_info:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy trạm với mã '{codename}'")
    
    # Always check eligibility even with valid session token
    can_visit = await external_api.can_visit_station(codename, jwt_token)
    
    if not can_visit:
        raise HTTPException(status_code=500, detail="Không thể kiểm tra tình trạng truy cập trạm")
    
    if can_visit.reason == "not yet":
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_type": "not_yet",
            "status_code": 403,
            "error_detail": "Bạn chưa đủ điều kiện để truy cập trạm này",
            "station_name": station_info.name,
            "codename": codename,
            "station_id": station_info.station_id
        })
    elif can_visit.reason == "conflict":
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_type": "conflict",
            "status_code": 409,
            "error_detail": "Đội đã bỏ qua trạm này và không thể truy cập lại cho đến khi hủy bỏ qua (trả phí)",
            "station_name": station_info.name,
            "codename": codename,
            "station_id": station_info.station_id
        })
    
    # Verify session token only after eligibility is confirmed
    session = await verify_game_session(session_token, station_info.station_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session không hợp lệ hoặc đã hết hạn")
    
    return templates.TemplateResponse("game.html", {
        "request": request,
        "station_id": station_info.station_id,
        "codename": codename,
        "station_name": station_info.name,
        "session_token": session_token
    })

@app.post("/game/{codename}/submit")
async def submit_game_result(
    codename: str,
    request: Request,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Submit game result and invalidate session"""
    data = await request.json()
    session_token = data.get("session_token")
    
    if not session_token:
        raise HTTPException(status_code=400, detail="Cần có session token")
    
    # Get JWT token and station info
    jwt_token = request.cookies.get("jwt_token")
    station_info = await external_api.get_station_by_codename(codename, jwt_token)
    
    if not station_info:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy trạm với mã '{codename}'")
    
    # Verify session token
    session = await verify_game_session(session_token, station_info.station_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session không hợp lệ hoặc đã hết hạn")
    
    # Verify session belongs to current user
    if session.username != current_user.username:
        raise HTTPException(status_code=403, detail="Session không thuộc về người dùng hiện tại")
    
    # Process game result and verify against game logic
    score = data.get("score", 0)
    completed = data.get("completed", False)
    answer = data.get("answer", "")  # Get submitted answer
    
    # Verify game-specific logic
    game_verified = await verify_game_logic(codename, data)
    
    # Log the result (you can save to database if needed)
    print(f"Game result: Team {current_user.team_name or current_user.username}, Station {station_info.station_id}, Score: {score}, Completed: {completed}, Verified: {game_verified}")
    
    # Nếu pass thì unlock puzzle, nếu không vẫn xóa session và coi như lượt chơi kết thúc
    if game_verified:
        # Get the appropriate PIN for this game
        pin = get_game_pin(codename)
        if pin and current_user.username:
            unlock_success = await external_api.unlock_puzzle(codename, pin, current_user.username)
            if unlock_success:
                print(f"Puzzle unlocked successfully for team {current_user.username}")
            else:
                print(f"Failed to unlock puzzle for team {current_user.username}")
    # Dù pass hay không đều xóa session
    await invalidate_game_session(session_token)
    return {
        "message": "Kết quả game đã được gửi thành công",
        "score": score,
        "completed": completed,
        "verified": game_verified,
        "puzzle_unlocked": game_verified  # Let frontend know if puzzle was unlocked
    }

# API endpoints for game servers to verify sessions
@app.get("/api/verify-session/{session_token}")
async def verify_session_api(session_token: str, station_id: str):
    """API endpoint for game servers to verify session tokens"""
    session = await verify_game_session(session_token, station_id)
    
    if not session:
        raise HTTPException(status_code=401, detail="Session không hợp lệ hoặc đã hết hạn")
    
    return {
        "valid": True,
        "user_id": session.user_id,
        "username": session.username,
        "station_id": session.station_id,
        "created_at": session.created_at
    }

@app.post("/api/invalidate-session/{session_token}")
async def invalidate_session_api(session_token: str):
    """API endpoint for game servers to invalidate session tokens"""
    await invalidate_game_session(session_token)
    return {"message": "Session đã được hủy thành công"}

@app.post("/game/{codename}/skip")
async def skip_game(
    codename: str,
    request: Request,
    current_user: UserResponse = Depends(get_current_user_from_cookie)
):
    """Skip the current game station"""
    # Check if user has team_id
    if not current_user.team_id:
        raise HTTPException(status_code=400, detail="Không tìm thấy ID đội của người dùng")
    
    # Get JWT token and station info to find the station_id
    jwt_token = request.cookies.get("jwt_token")
    station_info = await external_api.get_station_by_codename(codename, jwt_token)
    
    if not station_info:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy trạm với mã '{codename}'")
    
    # Find and invalidate any active session for this user and station
    existing_session = await find_active_session(current_user, station_info.station_id)
    if existing_session:
        await invalidate_game_session(existing_session.session_token)
    
    # Get the appropriate PIN for this game
    pin = get_game_pin(codename)
    if not pin:
        raise HTTPException(status_code=400, detail="Mã game không hợp lệ")

    # Skip the station using the specific PIN for this game and team_id
    skip_success = await external_api.skip_station(codename, pin, current_user.team_id)

    if not skip_success:
        raise HTTPException(status_code=500, detail="Không thể bỏ qua trạm")
    
    return {"message": "Trạm đã được bỏ qua thành công"}

def get_game_pin(codename: str) -> str:
    """Get the appropriate PIN for the domain game"""
    if codename == "ten-mien-de-thuong":
        return settings.TEN_MIEN_DE_THUONG_PIN
    return settings.SKIP_PIN  # Fallback to default PIN

async def verify_game_logic(codename: str, game_data: dict) -> bool:
    """Verify game-specific logic for domain classification game"""
    if codename != "ten-mien-de-thuong":
        return False
    
    # Check if game was completed and answers provided
    completed = game_data.get("completed", False)
    user_answers = game_data.get("answers", [])
    
    if not completed or not user_answers:
        return False
    
    # Verify domain classification answers using our verification API logic
    domains_to_verify = []
    for answer in user_answers:
        domain = answer.get("domain")
        user_classification = answer.get("is_legitimate")
        
        if not domain:
            continue
            
        # Check if domain is in our lists
        from domain_data import LEGITIMATE_DOMAINS, SUSPICIOUS_DOMAINS
        
        if domain in LEGITIMATE_DOMAINS:
            correct_classification = True
        elif domain in SUSPICIOUS_DOMAINS:
            correct_classification = False
        else:
            # Unknown domain, skip
            continue
            
        domains_to_verify.append({
            "domain": domain,
            "is_legitimate": correct_classification
        })
    
    # Verify answers
    result = verify_answers(user_answers, domains_to_verify)
    
    # Return True if user passed (more than 20 correct out of 30)
    return result["passed"]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
