import praw
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

# Reddit API credentials (replace with your actual credentials)
REDDIT_CLIENT_ID = "YOUR_CLIENT_ID"
REDDIT_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDDIT_USERNAME = "YOUR_USERNAME"
REDDIT_PASSWORD = "YOUR_PASSWORD"
REDDIT_USER_AGENT = "RecruitmentBot by /u/YOUR_USERNAME"

SUBREDDIT = "test"  # Replace with your target subreddit
POST_TITLE = "We're Hiring! Join Our Team at AutoRecruit"
POST_BODY = """
🚀 **AutoRecruit is looking for talented individuals!**

We are currently seeking passionate developers and recruiters to join our dynamic team.

**Open Positions:**
- Python Developer
- Recruitment Consultant
- Marketing Specialist

**How to Apply:**
Reply to this post or visit our website for more information.

Let's build the future of recruitment together!
"""

def post_recruitment_ad():
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=REDDIT_USER_AGENT,
    )
    subreddit = reddit.subreddit(SUBREDDIT)
    submission = subreddit.submit(POST_TITLE, selftext=POST_BODY)
    print(f"Posted at {datetime.datetime.now()}: {submission.title} (URL: {submission.url})")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Schedule every week (e.g., Monday at 9:00 AM UTC)
    scheduler.add_job(post_recruitment_ad, 'cron', day_of_week='mon', hour=9, minute=0)
    print("Reddit recruitment bot started. Posting weekly.")
    scheduler.start()