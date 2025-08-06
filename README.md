# 🤖 AutoRecruit - Weekly Reddit Bot

A Python Reddit bot that posts a weekly recruitment message to r/ClashOfClansRecruit every Monday at 13:00 UTC.

> 🔁 Built for `Scavengers | #2RUPQUQCJ` to maintain consistent and automated recruiting on Reddit.

---

## 📌 Features

- 🕒 Automatically posts once per week at **13:00 UTC on Mondays**
- 💾 Tracks last post date to prevent duplicates
- 🌐 Includes a lightweight Flask server to stay alive on platforms like Replit or Render
- 🔐 Uses environment variables for Reddit credentials
- 🔄 Runs continuously with hourly checks

---

## 📝 Example Post

**Title:**

**Body:**

> 🔥 **Join Scavengers – Competitive War & CWL Clan!** 🔥  
> We’re a serious, active war clan running back-to-back wars and pushing to improve our attacks. If you’re active, skilled, and want to grow, join us!  
>
> ✅ 30v30 CWL & back-to-back wars  
> ✅ Clan Games (1,000 pts) & Raid participation  
> ✅ No rushed bases – Must be improving  
> ✅ **Discord for war planning and communication**  
>
> 🔗 [Join now](https://link.clashofclans.com/en?action=OpenClanProfile&tag=2RUPQUQCJ)  
> 💬 DM for details!

---

## 🚀 Deployment Options

### 🌐 Render

1. Fork this repo and push to your GitHub
2. Create a **new Web Service** on [Render](https://render.com/)
3. Select your repository and branch (e.g., `main`)
4. Set build and start commands:
5. Add environment variables:
- `CLIENT_ID`
- `CLIENT_SECRET`
- `USERNAME`
- `PASSWORD`

---

## 🛠️ Configuration

| Setting        | Description                                   |
|----------------|-----------------------------------------------|
| `POST_HOUR_UTC`| Hour of day to post (UTC) — `13` = 1:00 PM    |
| `POST_DAY_UTC` | Day of week to post — `0` = Monday            |
| `LOG_FILE`     | File to track last post date                  |

---

## 📂 Files

- `main.py` — Main bot script  
- `last_post.json` — Log of last post date  
- `requirements.txt` — Python dependencies  
- `.env` — Add your Reddit credentials here (if running locally)  

---

## ✅ Requirements

- Python 3.7+
- Reddit account with script app access
- Subreddit permissions to post

Install dependencies:
```bash
pip install -r requirements.txt
