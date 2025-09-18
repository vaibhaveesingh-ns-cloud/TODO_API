from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .. import models, crud, auth, email_utils
from ..database import get_db
from ..rate_limit import RateLimiter, SessionManager, get_client_ip, get_user_agent
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str

class SessionInfo(BaseModel):
    id: int
    created_at: str
    last_activity: str
    expires_at: str
    ip_address: str

@router.post("/register", response_model=RegisterResponse)
def register(user_in: models.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username) or crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    user = crud.create_user(db, user_in.username, user_in.email, user_in.password)
    token = email_utils.generate_verification_token(user.email)
    email_utils.send_verification_email(user.email, token)
    return {"id": user.id, "username": user.username, "email": user.email}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = email_utils.confirm_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.activate_user(db, user)
    return {"message": "Email verified. You can now login."}

@router.post("/token", response_model=models.Token)
def login_for_token(request: Request, form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Get client info
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    username = form_data.username
    
    # Check rate limiting
    if not RateLimiter.check_login_attempts(db, username, ip_address):
        remaining_time = RateLimiter.get_lockout_time_remaining(db, username, ip_address)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many failed login attempts. Try again in {remaining_time} minutes."
        )
    
    # Authenticate user
    user = auth.authenticate_user(db, username, form_data.password)
    
    # Record login attempt
    if not user:
        RateLimiter.record_login_attempt(db, username, ip_address, user_agent, False)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    if not user.is_active:
        RateLimiter.record_login_attempt(db, username, ip_address, user_agent, False, user.id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")
    
    # Record successful login attempt
    RateLimiter.record_login_attempt(db, username, ip_address, user_agent, True, user.id)
    
    # Create session (this will invalidate any existing sessions)
    session = SessionManager.create_session(db, user.id, ip_address, user_agent)
    
    # Create access token with session reference
    access_token = auth.create_access_token(
        data={"sub": user.username}, 
        session_token=session.session_token
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=models.UserOut)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """Get current authenticated user information"""
    return current_user

@router.post("/logout")
def logout(request: Request, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Logout and invalidate current session"""
    # Extract session token from JWT
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            from jose import jwt
            payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
            session_token = payload.get("session_token")
            if session_token:
                SessionManager.invalidate_session(db, session_token)
        except:
            pass  # Token might be malformed, but we still want to respond with success
    
    return {"message": "Successfully logged out"}

@router.get("/sessions")
def get_active_sessions(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Get user's active sessions (for admin/debugging)"""
    sessions = db.query(models.UserSession).filter(
        models.UserSession.user_id == current_user.id,
        models.UserSession.is_active == True
    ).all()
    
    return {
        "active_sessions": len(sessions),
        "sessions": [{
            "id": s.id,
            "created_at": s.created_at,
            "last_activity": s.last_activity,
            "expires_at": s.expires_at,
            "ip_address": s.ip_address
        } for s in sessions]
    }
