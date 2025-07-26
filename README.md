# Game Login System Blueprint

A comprehensive FastAPI-based blueprint for integrating a unified login system across multiple games.

## Features

- **Unified Authentication**: Single login system for all games
- **JWT Token Management**: Secure token-based authentication with HTTP-only cookies
- **Payment Integration**: Support for game access payments and skip fees
- **Session Management**: Secure game session tokens that can't be manipulated by users
- **MongoDB Integration**: Persistent storage for sessions and user data
- **External API Integration**: Seamless integration with existing auth and payment services

## Architecture Overview

### Authentication Flow
1. User attempts to access a game
2. If not authenticated, redirected to login page
3. Login calls external `/auth/sign-in` API
4. JWT token stored in HTTP-only cookie
5. All subsequent requests validated via `/user/me` API

### Game Access Flow
1. Check eligibility via `/station/can-visit/{id}`
2. Handle different scenarios:
   - `"skip"`: Redirect to skip payment
   - `"not yet"`: Access denied
   - `"nothing"`: Proceed to game payment
3. Process payments via external APIs
4. Generate secure session token for game access
5. Invalidate session after game completion

## Project Structure

```
login_page/
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── auth.py              # Authentication utilities
├── database.py          # MongoDB connection and utilities
├── external_api.py      # External API client
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env                # Environment variables
└── templates/          # HTML templates
    ├── login.html      # Login page
    ├── games.html      # Game selection page
    ├── payment.html    # Payment page
    └── game.html       # Game session page
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MongoDB:
```bash
# Make sure MongoDB is running on localhost:27017
# Or update MONGODB_URL in .env file
```

3. Configure environment variables in `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=game_login_system
SECRET_KEY=your-super-secret-key-change-this-in-production
AUTH_API_BASE_URL=http://localhost:5000
STATION_API_BASE_URL=http://localhost:5000
```

4. Run the application:
```bash
python main.py
```

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Process login
- `POST /logout` - Logout user
- `GET /user/profile` - Get current user profile

### Game Flow
- `GET /games` - Game selection page
- `GET /game-flow/{station_id}` - Start game flow
- `GET /payment` - Payment page
- `POST /game-flow/{station_id}/unskip` - Unskip station (automatically pays)
- `POST /game-flow/{station_id}/pay-visit` - Pay for game access

### Game Session
- `GET /game/{station_id}` - Game page
- `POST /game/{station_id}/submit` - Submit game result (verifies answer and unlocks puzzle if correct)
- `GET /api/verify-session/{session_token}` - Verify session (for game servers)
- `POST /api/invalidate-session/{session_token}` - Invalidate session

## Game Flow Process

The application follows this complete flow:

1. **Login**: User authenticates with external auth API
2. **Game Selection**: User chooses from available games
3. **Eligibility Check**: System checks if user can access the game via `can-visit` API
4. **Unlocked Puzzle Check**: System checks if user has already completed this puzzle
5. **Payment**: If required, user pays for game access or unskip (using "Thẻ hồi sinh")
6. **Game Session**: Valid session created for gameplay
7. **Game Submission**: User submits answer, system verifies game-specific logic
8. **Puzzle Unlock**: If answer is correct, puzzle is automatically unlocked via external API
9. **Session Cleanup**: Game session invalidated after submission

## External API Integration

The system integrates with the following external APIs:

### Authentication API (`http://localhost:5000`)
- `POST /auth/sign-in` - User login
- `GET /user/me` - Get user information

### Station API (`http://localhost:5000`)
- `GET /station/can-visit/{codename}` - Check access eligibility by codename
- `POST /station/unskip` - Unskip station (automatically pays) with codename and PIN
- `GET /station/visit-price/{codename}` - Get game access price by codename  
- `POST /station/visit` - Pay for game access with codename and PIN

## Security Features

- **HTTP-only Cookies**: JWT tokens stored securely
- **Session Tokens**: Unguessable tokens for game authentication
- **Session Validation**: Server-side session verification
- **Automatic Invalidation**: Sessions cleared after game completion
- **User Verification**: Multiple layers of user authentication

## Database Schema

### Collections

#### `game_sessions`
```json
{
  "user_id": "string",
  "username": "string", 
  "station_id": "string",
  "session_token": "string",
  "created_at": "datetime",
  "is_active": "boolean"
}
```

#### `users` (optional for caching)
```json
{
  "username": "string",
  "user_id": "string",
  "last_login": "datetime"
}
```

## Usage Examples

### For Game Developers

1. **Redirect to Login**:
```javascript
// If user not authenticated
window.location.href = `/login?station_id=${stationId}`;
```

2. **Verify Game Session**:
```javascript
// In your game, verify the session token
const response = await fetch(`/api/verify-session/${sessionToken}?station_id=${stationId}`);
```

3. **Submit Game Results**:
```javascript
// After game completion
await fetch(`/game/${stationId}/submit`, {
    method: 'POST',
    body: JSON.stringify({
        session_token: sessionToken,
        score: playerScore,
        completed: true
    })
});
```

### For Integration

1. **Embed Login Check**:
```html
<!-- Add to your game pages -->
<script>
if (!document.cookie.includes('jwt_token')) {
    window.location.href = '/login?redirect=' + encodeURIComponent(window.location.href);
}
</script>
```

2. **Payment Flow Integration**:
The system automatically handles the payment flow based on the external API responses.

## Environment Configuration

### Development
```env
DEBUG=True
HOST=0.0.0.0
PORT=8000
SECRET_KEY=dev-secret-key
```

### Production
```env
DEBUG=False
HOST=0.0.0.0
PORT=8000
SECRET_KEY=super-secure-production-key
MONGODB_URL=mongodb://production-server:27017
```

## Customization

### Adding New Games
1. Add game cards to `templates/games.html`
2. Update station IDs in the game flow
3. Customize game templates as needed

### Payment Integration
The system is designed to work with any payment provider. Update the external API client in `external_api.py` to match your payment system.

### Session Management
Session tokens are automatically generated and managed. You can customize the token generation in `auth.py`.

## Error Handling

The system includes comprehensive error handling:
- Invalid credentials
- Expired sessions
- Payment failures
- Network errors
- Database connection issues

## Security Considerations

1. **HTTPS in Production**: Always use HTTPS in production
2. **Secret Key**: Use a strong, unique secret key
3. **Database Security**: Secure your MongoDB instance
4. **Rate Limiting**: Consider adding rate limiting for login attempts
5. **Session Timeouts**: Configure appropriate session timeouts

## Monitoring and Logging

The application includes:
- Health check endpoint (`/health`)
- Console logging for debugging
- Error tracking and reporting

## Contributing

1. Follow the existing code structure
2. Add appropriate error handling
3. Update documentation for new features
4. Test all authentication flows

This blueprint provides a solid foundation for integrating unified authentication across multiple games while maintaining security and user experience.
