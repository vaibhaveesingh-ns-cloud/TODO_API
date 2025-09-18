"""
Rate limiting and session management utilities
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from . import models, crud
import secrets
import hashlib

# Rate limiting configuration
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15
SESSION_TIMEOUT_MINUTES = 15
CLEANUP_INTERVAL_HOURS = 24

class RateLimiter:
    @staticmethod
    def check_login_attempts(db: Session, username: str, ip_address: str) -> bool:
        """Check if user/IP is rate limited"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        
        # Count failed attempts in the last LOCKOUT_DURATION_MINUTES
        failed_attempts = db.query(models.LoginAttempt).filter(
            and_(
                models.LoginAttempt.username == username,
                models.LoginAttempt.ip_address == ip_address,
                models.LoginAttempt.success == False,
                models.LoginAttempt.attempted_at > cutoff_time
            )
        ).count()
        
        return failed_attempts < MAX_LOGIN_ATTEMPTS
    
    @staticmethod
    def record_login_attempt(db: Session, username: str, ip_address: str, 
                           user_agent: str, success: bool, user_id: Optional[int] = None):
        """Record a login attempt"""
        attempt = models.LoginAttempt(
            user_id=user_id,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success
        )
        db.add(attempt)
        db.commit()
    
    @staticmethod
    def get_lockout_time_remaining(db: Session, username: str, ip_address: str) -> Optional[int]:
        """Get remaining lockout time in minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        
        last_failed_attempt = db.query(models.LoginAttempt).filter(
            and_(
                models.LoginAttempt.username == username,
                models.LoginAttempt.ip_address == ip_address,
                models.LoginAttempt.success == False,
                models.LoginAttempt.attempted_at > cutoff_time
            )
        ).order_by(models.LoginAttempt.attempted_at.desc()).first()
        
        if last_failed_attempt:
            unlock_time = last_failed_attempt.attempted_at + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            remaining = (unlock_time - datetime.utcnow()).total_seconds() / 60
            return max(0, int(remaining))
        
        return None

class SessionManager:
    @staticmethod
    def generate_session_token() -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_session(db: Session, user_id: int, ip_address: str, 
                      user_agent: str) -> models.UserSession:
        """Create a new session and invalidate existing ones"""
        # Invalidate all existing sessions for this user (single login enforcement)
        db.query(models.UserSession).filter(
            and_(
                models.UserSession.user_id == user_id,
                models.UserSession.is_active == True
            )
        ).update({"is_active": False})
        
        # Create new session
        session_token = SessionManager.generate_session_token()
        expires_at = datetime.utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        
        session = models.UserSession(
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def validate_session(db: Session, session_token: str) -> Optional[models.UserSession]:
        """Validate and update session activity"""
        session = db.query(models.UserSession).filter(
            and_(
                models.UserSession.session_token == session_token,
                models.UserSession.is_active == True,
                models.UserSession.expires_at > datetime.utcnow()
            )
        ).first()
        
        if session:
            # Update last activity and extend expiration
            session.last_activity = datetime.utcnow()
            session.expires_at = datetime.utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
            db.commit()
            
        return session
    
    @staticmethod
    def invalidate_session(db: Session, session_token: str):
        """Invalidate a specific session"""
        db.query(models.UserSession).filter(
            models.UserSession.session_token == session_token
        ).update({"is_active": False})
        db.commit()
    
    @staticmethod
    def invalidate_user_sessions(db: Session, user_id: int):
        """Invalidate all sessions for a user"""
        db.query(models.UserSession).filter(
            and_(
                models.UserSession.user_id == user_id,
                models.UserSession.is_active == True
            )
        ).update({"is_active": False})
        db.commit()
    
    @staticmethod
    def cleanup_expired_sessions(db: Session):
        """Clean up expired sessions and old login attempts"""
        # Remove expired sessions
        db.query(models.UserSession).filter(
            models.UserSession.expires_at < datetime.utcnow()
        ).update({"is_active": False})
        
        # Remove old login attempts (older than 24 hours)
        cutoff_time = datetime.utcnow() - timedelta(hours=CLEANUP_INTERVAL_HOURS)
        db.query(models.LoginAttempt).filter(
            models.LoginAttempt.attempted_at < cutoff_time
        ).delete()
        
        db.commit()

def get_client_ip(request: Request) -> str:
    """Extract client IP address from request"""
    # Check for forwarded headers first (for proxy/load balancer scenarios)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct connection IP
    return request.client.host if request.client else "unknown"

def get_user_agent(request: Request) -> str:
    """Extract user agent from request"""
    return request.headers.get("User-Agent", "unknown")