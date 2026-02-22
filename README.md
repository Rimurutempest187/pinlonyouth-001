# ⛪ Church Community Telegram Bot
### Create by : PINLON-YOUTH

## 📁 File Structure
```
telegram-bot/
├── bot.py              # Main entry point
├── config.py           # Configuration (Token, Admin IDs)
├── database.py         # JSON-based data storage
├── handlers/
│   ├── __init__.py
│   ├── start.py        # /start - Welcome message
│   ├── admin.py        # /edit - Admin commands list
│   ├── about.py        # /about, /edabout
│   ├── contact.py      # /contact, /edcontact
│   ├── verse.py        # /verse, /edverse
│   ├── events.py       # /events, /edevents
│   ├── birthday.py     # /birthday, /edbirthday
│   ├── pray.py         # /pray, /praylist
│   ├── quiz.py         # /quiz, /edquiz, /tops, /set
│   ├── broadcast.py    # /broadcast
│   ├── stats.py        # /stats
│   ├── report.py       # /report
│   └── backup.py       # /backup, /restore, /allclear
├── utils/
│   ├── __init__.py
│   ├── decorators.py   # Admin check decorator
│   └── scheduler.py    # Daily verse auto sender
├── data/               # JSON data storage (auto-created)
├── requirements.txt
└── README.md
```

## 🚀 Setup & Run

### 1. Install Python 3.10+

### 2. Install Dependencies
```bash
cd telegram-bot
pip install -r requirements.txt
```

### 3. Configuration
`config.py` ဖိုင်ကို ဖွင့်ပြီး:

1. **BOT_TOKEN** - BotFather မှ ရရှိသော Token ထည့်ပါ
2. **ADMIN_IDS** - Admin Telegram User IDs ထည့်ပါ

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [123456789, 987654321]  # Your Telegram user IDs
```

> 💡 Telegram User ID ရရှိရန် @userinfobot ကို message ပို့ပါ။

### 4. Run Bot
```bash
python bot.py
```

## 📋 Commands

### 👤 User Commands
| Command | Description |
|---------|-------------|
| `/start` | Bot ကို စတင်အသုံးပြုခြင်း |
| `/about` | အသင်းတော်အကြောင်း |
| `/contact` | ဆက်သွယ်ရန် ဖုန်းနံပါတ်များ |
| `/verse` | ယနေ့အတွက် ကျမ်းချက် |
| `/events` | လာမည့် အစီအစဉ်များ |
| `/birthday` | ယခုလ မွေးနေ့စာရင်း |
| `/pray <text>` | ဆုတောင်းချက် ပေးပို့ရန် |
| `/praylist` | ဆုတောင်းချက်စာရင်း |
| `/quiz` | Quiz ဖြေရန် |
| `/tops` | Quiz Ranking |
| `/report <text>` | အကြောင်းအရာ တင်ပြရန် |

### 🔐 Admin Commands
| Command | Description |
|---------|-------------|
| `/edit` | Admin commands list ပြရန် |
| `/edabout` | အသင်းတော်အကြောင်း ပြင်ဆင်ရန် |
| `/edcontact` | ဆက်သွယ်ရန် ပြင်ဆင်ရန် |
| `/edverse` | ကျမ်းချက် ထည့်ရန် |
| `/edevents` | အစီအစဉ် ပြင်ဆင်ရန် |
| `/edbirthday` | မွေးနေ့စာရင်း ပြင်ဆင်ရန် |
| `/edquiz` | Quiz ထည့်ရန် |
| `/set <n>` | Quiz trigger message count |
| `/broadcast` | Group များသို့ သတင်းပို့ |
| `/stats` | Users/Groups စာရင်း |
| `/backup` | Data Backup |
| `/restore` | Data ပြန်ယူရန် |
| `/allclear` | Data အားလုံး ဖျက်ရန် |

## ✨ Features

- 🔐 **Admin System** - Admin-only commands with decorator
- 📖 **Daily Verse** - Auto morning & night verse to groups
- 🧠 **Auto Quiz** - Message count triggers auto quiz in groups
- 🏆 **Quiz Ranking** - Track scores with leaderboard
- 📢 **Broadcast** - Send text + photos to all groups
- 💾 **Backup/Restore** - Protect against data loss
- 🙏 **Prayer Requests** - Community prayer support
- 📊 **Statistics** - Track users and groups

## ⚙️ Daily Verse Schedule
- 🌅 Morning: 6:00 AM (UTC)
- 🌙 Night: 8:00 PM (UTC)

> `config.py` တွင် အချိန်ပြောင်းလဲနိုင်ပါသည်။

---
🤖 **Create by : PINLON-YOUTH**
