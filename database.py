"""
Church Community Telegram Bot - Database (JSON-based storage)
Create by : PINLON-YOUTH
"""

import json
import os
import shutil
from datetime import datetime
from config import DATA_DIR

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Data file paths
ABOUT_FILE = os.path.join(DATA_DIR, "about.json")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")
VERSES_FILE = os.path.join(DATA_DIR, "verses.json")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
BIRTHDAYS_FILE = os.path.join(DATA_DIR, "birthdays.json")
PRAYERS_FILE = os.path.join(DATA_DIR, "prayers.json")
QUIZZES_FILE = os.path.join(DATA_DIR, "quizzes.json")
SCORES_FILE = os.path.join(DATA_DIR, "scores.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
GROUPS_FILE = os.path.join(DATA_DIR, "groups.json")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
MSG_COUNT_FILE = os.path.join(DATA_DIR, "msg_count.json")

BACKUP_DIR = os.path.join(DATA_DIR, "backups")


def _read_json(filepath, default=None):
    """Read JSON file safely."""
    if default is None:
        default = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return default


def _write_json(filepath, data):
    """Write data to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─── About ───────────────────────────────────────────────
def get_about():
    data = _read_json(ABOUT_FILE, {"text": "အချက်အလက် မရှိသေးပါ။"})
    return data.get("text", "အချက်အလက် မရှိသေးပါ။")


def set_about(text):
    _write_json(ABOUT_FILE, {"text": text})


# ─── Contacts ────────────────────────────────────────────
def get_contacts():
    return _read_json(CONTACTS_FILE, {"contacts": []}).get("contacts", [])


def set_contacts(contacts_list):
    _write_json(CONTACTS_FILE, {"contacts": contacts_list})


# ─── Verses ──────────────────────────────────────────────
def get_verses():
    return _read_json(VERSES_FILE, {"verses": []}).get("verses", [])


def add_verse(verse_text):
    data = _read_json(VERSES_FILE, {"verses": []})
    data["verses"].append(verse_text)
    _write_json(VERSES_FILE, data)


def set_verses(verses_list):
    _write_json(VERSES_FILE, {"verses": verses_list})


# ─── Events ──────────────────────────────────────────────
def get_events():
    return _read_json(EVENTS_FILE, {"events": []}).get("events", [])


def set_events(events_list):
    _write_json(EVENTS_FILE, {"events": events_list})


# ─── Birthdays ───────────────────────────────────────────
def get_birthdays():
    return _read_json(BIRTHDAYS_FILE, {"birthdays": []}).get("birthdays", [])


def set_birthdays(birthdays_list):
    _write_json(BIRTHDAYS_FILE, {"birthdays": birthdays_list})


# ─── Prayers ─────────────────────────────────────────────
def get_prayers():
    return _read_json(PRAYERS_FILE, {"prayers": []}).get("prayers", [])


def add_prayer(username, text):
    data = _read_json(PRAYERS_FILE, {"prayers": []})
    data["prayers"].append({
        "username": username,
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    _write_json(PRAYERS_FILE, data)


def clear_prayers():
    _write_json(PRAYERS_FILE, {"prayers": []})


# ─── Quizzes ─────────────────────────────────────────────
def get_quizzes():
    return _read_json(QUIZZES_FILE, {"quizzes": []}).get("quizzes", [])


def add_quiz(question, options, correct_answer):
    """
    options: dict like {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer: "A", "B", "C", or "D"
    """
    data = _read_json(QUIZZES_FILE, {"quizzes": []})
    data["quizzes"].append({
        "question": question,
        "options": options,
        "answer": correct_answer.upper()
    })
    _write_json(QUIZZES_FILE, data)


def set_quizzes(quizzes_list):
    _write_json(QUIZZES_FILE, {"quizzes": quizzes_list})


# ─── Scores ──────────────────────────────────────────────
def get_scores():
    return _read_json(SCORES_FILE, {})


def add_score(user_id, username, points=1):
    data = _read_json(SCORES_FILE, {})
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"username": username, "score": 0}
    data[uid]["score"] += points
    data[uid]["username"] = username  # Update username
    _write_json(SCORES_FILE, data)


def get_top_scores(limit=10):
    data = _read_json(SCORES_FILE, {})
    sorted_scores = sorted(data.items(), key=lambda x: x[1]["score"], reverse=True)
    return sorted_scores[:limit]


# ─── Users & Groups ─────────────────────────────────────
def register_user(user_id, username, first_name):
    data = _read_json(USERS_FILE, {})
    uid = str(user_id)
    data[uid] = {
        "username": username or "",
        "first_name": first_name or "",
        "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    _write_json(USERS_FILE, data)


def get_users():
    return _read_json(USERS_FILE, {})


def register_group(chat_id, title):
    data = _read_json(GROUPS_FILE, {})
    gid = str(chat_id)
    data[gid] = {
        "title": title or "",
        "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    _write_json(GROUPS_FILE, data)


def get_groups():
    return _read_json(GROUPS_FILE, {})


# ─── Reports ────────────────────────────────────────────
def add_report(user_id, username, text):
    data = _read_json(REPORTS_FILE, {"reports": []})
    data["reports"].append({
        "user_id": user_id,
        "username": username,
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    _write_json(REPORTS_FILE, data)


def get_reports():
    return _read_json(REPORTS_FILE, {"reports": []}).get("reports", [])


# ─── Settings ───────────────────────────────────────────
def get_settings():
    return _read_json(SETTINGS_FILE, {"quiz_msg_count": 5})


def set_quiz_msg_count(count):
    data = _read_json(SETTINGS_FILE, {"quiz_msg_count": 5})
    data["quiz_msg_count"] = count
    _write_json(SETTINGS_FILE, data)


def get_quiz_msg_count():
    data = get_settings()
    return data.get("quiz_msg_count", 5)


# ─── Message Counter ────────────────────────────────────
def get_msg_counts():
    return _read_json(MSG_COUNT_FILE, {})


def increment_msg_count(chat_id):
    data = _read_json(MSG_COUNT_FILE, {})
    cid = str(chat_id)
    data[cid] = data.get(cid, 0) + 1
    _write_json(MSG_COUNT_FILE, data)
    return data[cid]


def reset_msg_count(chat_id):
    data = _read_json(MSG_COUNT_FILE, {})
    data[str(chat_id)] = 0
    _write_json(MSG_COUNT_FILE, data)


# ─── Backup & Restore ───────────────────────────────────
def backup_data():
    """Create a backup of all data files."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)

    files_to_backup = [
        ABOUT_FILE, CONTACTS_FILE, VERSES_FILE, EVENTS_FILE,
        BIRTHDAYS_FILE, PRAYERS_FILE, QUIZZES_FILE, SCORES_FILE,
        USERS_FILE, GROUPS_FILE, REPORTS_FILE, SETTINGS_FILE, MSG_COUNT_FILE
    ]

    backed_up = 0
    for filepath in files_to_backup:
        if os.path.exists(filepath):
            shutil.copy2(filepath, backup_path)
            backed_up += 1

    return backup_path, backed_up


def restore_data():
    """Restore from the latest backup."""
    if not os.path.exists(BACKUP_DIR):
        return False, "Backup မရှိပါ။"

    backups = sorted(os.listdir(BACKUP_DIR), reverse=True)
    if not backups:
        return False, "Backup မရှိပါ။"

    latest = os.path.join(BACKUP_DIR, backups[0])
    restored = 0
    for filename in os.listdir(latest):
        src = os.path.join(latest, filename)
        dst = os.path.join(DATA_DIR, filename)
        shutil.copy2(src, dst)
        restored += 1

    return True, f"✅ Backup ({backups[0]}) မှ ဖိုင် {restored} ခု ပြန်လည်ရယူပြီးပါပြီ။"


def clear_all_data():
    """Delete all data files."""
    files_to_clear = [
        ABOUT_FILE, CONTACTS_FILE, VERSES_FILE, EVENTS_FILE,
        BIRTHDAYS_FILE, PRAYERS_FILE, QUIZZES_FILE, SCORES_FILE,
        USERS_FILE, GROUPS_FILE, REPORTS_FILE, SETTINGS_FILE, MSG_COUNT_FILE
    ]
    cleared = 0
    for filepath in files_to_clear:
        if os.path.exists(filepath):
            os.remove(filepath)
            cleared += 1
    return cleared
