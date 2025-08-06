import praw
import time
import json
import os
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# === Reddit Credentials ===
reddit = praw.Reddit()
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    username=os.getenv('USERNAME'),
    password=os.getenv('PASSWORD'),
    user_agent='ScavengersWeeklyBot by u/joinscvgers'

# === Settings ===
SUBREDDIT_NAME = 'ClashOfClansRecruit'
POST_HOUR_UTC = 13  # 13:00 UTC every Monday
POST_DAY_UTC = 0    # 0 = Monday
LOG_FILE = "last_post.json"

TITLE = "[Recruiting] Scavengers | #2RUPQUQCJ | TH11+ | Lvl 10 | Social/War/Clan Games/Clan Capital | Independent"
BODY = """
🔥 **Join Scavengers – Competitive War & CWL Clan!** 🔥

We’re a serious, active war clan running back-to-back wars and pushing to improve our attacks. If you’re active, skilled, and want to grow, join us!

✅ 30v30 CWL & back-to-back wars (heroes required so opt out when upgrading)  
✅ Clan Games (1,000 pts) & Raid participation required  
✅ Must have 1-2 solid war attack strategies (No E-Drag spam)  
✅ No rushed bases – Must be improving  
✅ Follow attack plans & contribute to the team  
✅ **Discord for war planning and communication**

🔗 [Join now](https://link.clashofclans.com/en?action=OpenClanProfile&tag=2RUPQUQCJ)  
💬 DM me for more details!

---

^I'm ^a ^bot ^posting ^weekly. ^Message ^mods ^if ^this ^post ^violates ^any ^rules.
"""

# === Web server to keep Replit alive ===
app = Flask('')
@app.route('/')
def home():
    return "I'm alive!"
def run_web():
    app.run(host='0.0.0.0', port=8080)

# === Bot Functions ===
def load_last_post_date():
    if not os.path.exists(LOG_FILE):
        return None
    with open(LOG_FILE, 'r') as f:
        data = json.load(f)
        return datetime.strptime(data['last_post'], "%Y-%m-%d")

def save_last_post_date():
    with open(LOG_FILE, 'w') as f:
        json.dump({'last_post': datetime.utcnow().strftime("%Y-%m-%d")}, f)

def should_post():
    now = datetime.utcnow()
    last_post = load_last_post_date()
    if now.weekday() != POST_DAY_UTC or now.hour != POST_HOUR_UTC:
        return False
    if last_post is None or (now.date() - last_post.date()).days >= 7:
        return True
    return False

def post_to_reddit():
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    subreddit.submit(title=TITLE, selftext=BODY)
    print(f"✅ Posted to r/{SUBREDDIT_NAME} at {datetime.utcnow().isoformat()}")
    save_last_post_date()

# === Main Loop ===
def run_bot():
    while True:
        if should_post():
            try:
                post_to_reddit()
            except Exception as e:
                print(f"❌ Error posting: {e}")
        else:
            print("⏳ Not time to post yet.")
        time.sleep(3600)  # Check every hour

# === Start Everything ===
Thread(target=run_web).start()
run_bot()
