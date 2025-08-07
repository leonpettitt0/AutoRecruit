# 🤖 AutoRecruit – Weekly COC Reddit Recruitment Bot

AutoRecruit is a Python bot that automatically posts a recruitment message to [r/ClashOfClansRecruit](https://www.reddit.com/r/ClashOfClansRecruit) every Monday at **13:00 UTC**.

> 🔁 Originally built for the `Scavengers | #2RUPQUQCJ` clan in the Clash of Clans mobile game to maintain consistent, automated Reddit recruiting.

---

## 📌 Features

- 🗓️ Posts automatically every **Monday at 13:00 UTC**
- 🔄 Continuously runs and **counts down until the next scheduled post**
- 💬 **Displays the upcoming post content and title** in advance
- 🧠 Prevents duplicate posts by logging the last post time
- 🌐 Includes a lightweight Flask server for cloud hosting (Replit/Render)
- 🔐 Uses environment variables for secure credential management

---

## 📝 Example Post

**Title:**  
`[Recruiting] Scavengers | #2RUPQUQCJ | TH11+ | Lvl 10 | Social/War/Clan Games/Clan Capital | Independent`

**Body:**
`Join Scavengers – Competitive War & CWL Clan!** 🔥`
>   
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

## 🚀 Deployment (Render)

1. Fork this repository to your GitHub
2. Create a **Web Service** on [Render](https://render.com/)
3. Connect your GitHub repo and select the branch (e.g. `main`)
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
5. Add the following **Environment Variables**:
   - `CLIENT_ID`
   - `CLIENT_SECRET`
   - `USERNAME`
   - `PASSWORD`

---

## ⚙️ Configuration

| Variable         | Description                                 |
|------------------|---------------------------------------------|
| `POST_HOUR_UTC`  | Hour to post (UTC) — e.g., `13` = 1:00 PM   |
| `POST_DAY_UTC`   | Day to post — `0` = Monday, `6` = Sunday    |
| `LOG_FILE`       | File to store the last post date            |

---

## 📁 Project Structure

- `main.py` – Core bot logic  
- `last_post.json` – Log of last post timestamp  
- `requirements.txt` – Python dependencies  
- `.env` – Local credentials file (optional for local dev)

---

## ✅ Requirements

- Python 3.7+
- Reddit script app credentials ([Create here](https://www.reddit.com/prefs/apps))
- Subreddit permission to post

Install dependencies:
```bash
pip install -r requirements.txt
