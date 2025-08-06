import praw
import time
import json
import os
import logging
from datetime import datetime, timedelta
from threading import Lock
from config import Config

logger = logging.getLogger(__name__)

class RedditBot:
    def __init__(self):
        self.reddit = None
        self.running = False
        self.last_error = None
        self.post_lock = Lock()
        self.logs = []
        self.max_logs = 100
        
        # Initialize Reddit connection
        self._init_reddit()
    
    def _init_reddit(self):
        """Initialize Reddit API connection"""
        try:
            # Check if all required credentials are present
            client_id = os.getenv('REDDIT_CLIENT_ID', '')
            client_secret = os.getenv('REDDIT_CLIENT_SECRET', '')
            username = os.getenv('REDDIT_USERNAME', '')
            password = os.getenv('REDDIT_PASSWORD', '')
            
            if not all([client_id, client_secret, username, password]):
                missing = [var for var, val in [
                    ('REDDIT_CLIENT_ID', client_id),
                    ('REDDIT_CLIENT_SECRET', client_secret), 
                    ('REDDIT_USERNAME', username),
                    ('REDDIT_PASSWORD', password)
                ] if not val]
                raise Exception(f"Missing Reddit credentials: {', '.join(missing)}")
            
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=os.getenv('REDDIT_USER_AGENT', 'ScavengersWeeklyBot by u/joinscvgers')
            )
            logger.info("Reddit API initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit API: {e}")
            self.last_error = str(e)
    
    def _log(self, message, level='INFO'):
        """Add log entry"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message
        }
        self.logs.append(log_entry)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        
        # Also log to Python logger
        getattr(logger, level.lower())(message)
    
    def load_last_post_date(self):
        """Load the last post date from file"""
        if not os.path.exists(Config.LOG_FILE):
            return None
        try:
            with open(Config.LOG_FILE, 'r') as f:
                data = json.load(f)
                return datetime.strptime(data['last_post'], "%Y-%m-%d %H:%M:%S")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self._log(f"Error loading last post date: {e}", 'WARNING')
            return None
    
    def save_last_post_date(self, post_time=None):
        """Save the last post date to file"""
        if post_time is None:
            post_time = datetime.utcnow()
        
        data = {
            'last_post': post_time.strftime("%Y-%m-%d %H:%M:%S"),
            'subreddit': Config.SUBREDDIT_NAME,
            'title': Config.TITLE
        }
        
        try:
            with open(Config.LOG_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            self._log(f"Saved last post date: {post_time}")
        except Exception as e:
            self._log(f"Error saving last post date: {e}", 'ERROR')
    
    def should_post(self):
        """Check if it's time to post"""
        now = datetime.utcnow()
        
        # Check if it's the right day and hour
        if now.weekday() != Config.POST_DAY_UTC or now.hour != Config.POST_HOUR_UTC:
            return False, f"Not posting time. Current: {now.strftime('%A %H:%M UTC')}. Target: Monday {Config.POST_HOUR_UTC:02d}:00 UTC"
        
        # Check if we've already posted this week
        last_post = self.load_last_post_date()
        if last_post is None:
            return True, "No previous post found"
        
        days_since_last = (now - last_post).days
        if days_since_last >= 7:
            return True, f"Last post was {days_since_last} days ago"
        else:
            return False, f"Already posted this week. Last post: {last_post.strftime('%Y-%m-%d %H:%M UTC')}"
    
    def post_to_reddit(self):
        """Post to Reddit"""
        if not self.reddit:
            raise Exception("Reddit API not initialized")
        
        with self.post_lock:
            try:
                subreddit = self.reddit.subreddit(Config.SUBREDDIT_NAME)
                submission = subreddit.submit(title=Config.TITLE, selftext=Config.BODY)
                
                post_time = datetime.utcnow()
                self.save_last_post_date(post_time)
                
                message = f"Posted to r/{Config.SUBREDDIT_NAME} - {submission.url}"
                self._log(message)
                return True, message
                
            except Exception as e:
                error_msg = f"Error posting to Reddit: {str(e)}"
                self._log(error_msg, 'ERROR')
                self.last_error = error_msg
                return False, error_msg
    
    def manual_post(self):
        """Manually trigger a post"""
        self._log("Manual post triggered")
        return self.post_to_reddit()
    
    def test_reddit_connection(self):
        """Test Reddit API connection"""
        try:
            if not self.reddit:
                return False, "Reddit API not initialized"
            
            # Try to access user info
            user = self.reddit.user.me()
            if user and hasattr(user, 'name'):
                message = f"Connected as u/{user.name}"
            else:
                message = "Connected to Reddit API successfully"
            self._log(f"Reddit connection test successful: {message}")
            return True, message
            
        except Exception as e:
            error_str = str(e)
            if "invalid_grant" in error_str:
                error_msg = "Authentication failed: Invalid username/password combination. Please check your Reddit credentials."
            elif "401" in error_str or "Unauthorized" in error_str:
                error_msg = "Authentication failed: Invalid client ID or secret. Please check your Reddit app credentials."
            else:
                error_msg = f"Reddit connection test failed: {error_str}"
            
            self._log(error_msg, 'ERROR')
            self.last_error = error_msg
            return False, error_msg
    
    def get_status(self):
        """Get current bot status"""
        last_post = self.load_last_post_date()
        should_post, post_message = self.should_post()
        
        return {
            'running': self.running,
            'reddit_connected': self.reddit is not None,
            'last_error': self.last_error,
            'should_post': should_post,
            'post_message': post_message,
            'last_check': datetime.utcnow().isoformat()
        }
    
    def get_last_post_info(self):
        """Get information about the last post"""
        last_post = self.load_last_post_date()
        if last_post:
            return {
                'date': last_post.strftime('%Y-%m-%d %H:%M UTC'),
                'days_ago': (datetime.utcnow() - last_post).days
            }
        return None
    
    def get_next_post_time(self):
        """Calculate next scheduled post time"""
        now = datetime.utcnow()
        
        # Calculate next scheduled post day/hour (Config.POST_DAY_UTC uses Python's weekday: Monday=0, Sunday=6)
        days_ahead = (Config.POST_DAY_UTC - now.weekday()) % 7
        next_post = now + timedelta(days=days_ahead)
        next_post = next_post.replace(hour=Config.POST_HOUR_UTC, minute=0, second=0, microsecond=0)
        if next_post <= now:
            next_post += timedelta(days=7)
        return next_post
    
    def get_recent_logs(self):
        """Get recent log entries"""
        return list(reversed(self.logs[-50:]))  # Last 50 logs, newest first
    
    def run(self):
        """Main bot loop"""
        self.running = True
        self._log("Bot started")
        
        while self.running:
            try:
                should_post, message = self.should_post()
                
                if should_post:
                    self._log("Time to post!")
                    success, post_message = self.post_to_reddit()
                    if success:
                        self._log(f"Posted successfully: {post_message}")
                    else:
                        self._log(f"Post failed: {post_message}", 'ERROR')
                else:
                    self._log(f"Not posting: {message}", 'DEBUG')
                
                # Wait 1 hour before checking again
                time.sleep(3600)
                
            except Exception as e:
                error_msg = f"Error in bot loop: {str(e)}"
                self._log(error_msg, 'ERROR')
                self.last_error = error_msg
                time.sleep(300)  # Wait 5 minutes on error
    
    def stop(self):
        """Stop the bot"""
        self.running = False
        self._log("Bot stopped")
