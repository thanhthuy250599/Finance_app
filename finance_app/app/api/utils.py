import json
import os
from threading import Lock
from typing import Any, Dict, List

_io_lock = Lock()


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def read_json(path: str, default: Any) -> Any:
    ensure_dir(os.path.dirname(path))
    if not os.path.exists(path):
        return default
    with _io_lock:
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default


def write_json(path: str, data: Any) -> None:
    ensure_dir(os.path.dirname(path))
    tmp_path = path + ".tmp"
    with _io_lock:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)


def users_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "users.json")


def user_data_dir(username: str) -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "user_data", username)


def month_key(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"






