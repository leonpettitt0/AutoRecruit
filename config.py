import os

class Config:
    # Reddit Settings
    SUBREDDIT_NAME = 'ClashOfClansRecruit'
    POST_HOUR_UTC = 13  # 13:00 UTC every Monday
    POST_DAY_UTC = 0    # 0 = Monday
    LOG_FILE = "last_post.json"
    
    # Post Content
    TITLE = "[Recruiting] Scavengers | #2RUPQUQCJ | TH11+ | Lvl 10 | Social/War/Clan Games/Clan Capital | Independent"
    
    BODY = """🔥 **Join Scavengers – Competitive War & CWL Clan!** 🔥

We're a serious, active war clan running back-to-back wars and pushing to improve our attacks. If you're active, skilled, and want to grow, join us!

✅ 30v30 CWL & back-to-back wars (heroes required so opt out when upgrading)  
✅ Clan Games (1,000 pts) & Raid participation required  
✅ Must have 1-2 solid war attack strategies (No E-Drag spam)  
✅ No rushed bases – Must be improving  
✅ Follow attack plans & contribute to the team  
✅ **Discord for war planning and communication**

🔗 [Join now](https://link.clashofclans.com/en?action=OpenClanProfile&tag=2RUPQUQCJ)  
💬 DM me for more details!

---

^I'm ^a ^bot ^posting ^weekly. ^Message ^mods ^if ^this ^post ^violates ^any ^rules."""

    # Environment Variables Required
    REQUIRED_ENV_VARS = [
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET', 
        'REDDIT_USERNAME',
        'REDDIT_PASSWORD'
    ]
    
    @classmethod
    def check_environment(cls):
        """Check if all required environment variables are set"""
        missing = []
        for var in cls.REQUIRED_ENV_VARS:
            if not os.getenv(var):
                missing.append(var)
        return missing
