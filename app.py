import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from threading import Thread
from bot import RedditBot
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize bot
bot = RedditBot()
bot_thread = None

def start_bot():
    """Start the bot in a background thread"""
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = Thread(target=bot.run, daemon=True)
        bot_thread.start()
        logger.info("Bot thread started")

@app.route('/')
def dashboard():
    next_post_time = bot.get_next_post_time()  # Should return a datetime object
    if isinstance(next_post_time, datetime):
        next_post_time_str = next_post_time.isoformat()
    else:
        next_post_time_str = None
        if next_post_time is not None:
            logger.warning(f"Expected datetime, got {type(next_post_time)}: {next_post_time}")
    return render_template(
        "index.html",
        title=Config.TITLE,
        body=Config.BODY,
        next_post_time=next_post_time_str
    )

@app.route('/manual_post', methods=['POST'])
def manual_post():
    """Trigger a manual post"""
    try:
        success, message = bot.manual_post()
        if success:
            flash(f"Post successful: {message}", "success")
        else:
            flash(f"Post failed: {message}", "error")
    except Exception as e:
        logger.error(f"Manual post error: {e}")
        flash(f"Manual post error: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route('/test_connection')
def test_connection():
    """Test Reddit API connection"""
    try:
        success, message = bot.test_reddit_connection()
        if success:
            flash(f"Connection successful: {message}", "success")
        else:
            flash(f"Connection failed: {message}", "error")
    except Exception as e:
        logger.error(f"Connection test error: {e}")
        flash(f"Connection test error: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    try:
        status = bot.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs')
def logs():
    """View recent logs"""
    try:
        logs = bot.get_recent_logs()
        return render_template('logs.html', logs=logs)
    except Exception as e:
        logger.error(f"Error loading logs: {e}")
        flash(f"Error loading logs: {str(e)}", "error")
        return redirect(url_for('index'))

# Start the bot when the app starts
start_bot()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
