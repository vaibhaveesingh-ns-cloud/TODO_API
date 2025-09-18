"""
Background task scheduler for session cleanup and maintenance
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from .rate_limit import SessionManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundScheduler:
    def __init__(self):
        self.running = False
        self.cleanup_task = None
    
    async def start(self):
        """Start the background scheduler"""
        if self.running:
            return
        
        self.running = True
        self.cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("Background scheduler started")
    
    async def stop(self):
        """Stop the background scheduler"""
        self.running = False
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        logger.info("Background scheduler stopped")
    
    async def _cleanup_loop(self):
        """Main cleanup loop - runs every 5 minutes"""
        while self.running:
            try:
                await self._perform_cleanup()
                # Wait 5 minutes before next cleanup
                await asyncio.sleep(300)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {str(e)}")
                # Wait 1 minute before retrying on error
                await asyncio.sleep(60)
    
    async def _perform_cleanup(self):
        """Perform session and login attempt cleanup"""
        db = SessionLocal()
        try:
            logger.info("Starting session cleanup...")
            SessionManager.cleanup_expired_sessions(db)
            logger.info("Session cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
        finally:
            db.close()

# Global scheduler instance
scheduler = BackgroundScheduler()

async def start_scheduler():
    """Start the background scheduler"""
    await scheduler.start()

async def stop_scheduler():
    """Stop the background scheduler"""
    await scheduler.stop()
