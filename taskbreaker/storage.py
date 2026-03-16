"""Enkel JSON-lagring för uppgifter och steg."""

import json
import os

DATA_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "taskbreaker")
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_tasks() -> list[dict]:
    """Ladda sparade uppgifter från disk."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks: list[dict]):
    """Spara uppgifter till disk."""
    _ensure_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
