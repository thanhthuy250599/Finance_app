import os
from datetime import datetime
from typing import Dict, Optional

from .utils import read_json, write_json


def _limits_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "account_types.json")


def _ai_log_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "ai_call_log.json")


def _reset_log_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "reset_log.json")


def get_plan_limits(plan: str) -> Dict:
    cfg = read_json(_limits_path(), {})
    return cfg.get(plan, cfg.get("free", {}))


def should_reset_month(last_month: Optional[str], tz: str = "Asia/Ho_Chi_Minh") -> bool:
    # Simplified: ignore tz for now
    now_key = datetime.utcnow().strftime("%Y-%m")
    return last_month != now_key


def log_ai_call(entry: Dict) -> None:
    log = read_json(_ai_log_path(), [])
    log.append(entry)
    write_json(_ai_log_path(), log)


def log_reset(username: str, kind: str) -> None:
    log = read_json(_reset_log_path(), [])
    log.append({"username": username, "kind": kind, "ts": datetime.utcnow().isoformat()})
    write_json(_reset_log_path(), log)


def ensure_usage_fields(user: Dict) -> Dict:
    user.setdefault("plan_usage", {})
    for key in ("ai_month", "ai_day", "voice_month"):
        user["plan_usage"].setdefault(key, 0)
    return user


def reset_month_if_needed(user: Dict, username: str) -> None:
    if should_reset_month(user.get("last_reset_month")):
        ensure_usage_fields(user)
        user["plan_usage"]["ai_month"] = 0
        user["plan_usage"]["voice_month"] = 0
        user["last_reset_month"] = datetime.utcnow().strftime("%Y-%m")
        log_reset(username, "ai_month")
        log_reset(username, "voice_month")


def reset_day_if_needed(user: Dict, username: str) -> None:
    today_key = datetime.utcnow().strftime("%Y-%m-%d")
    if user.get("last_reset_day") != today_key:
        ensure_usage_fields(user)
        user["plan_usage"]["ai_day"] = 0
        user["last_reset_day"] = today_key
        log_reset(username, "ai_day")


def check_ai_quota(user: Dict, plan_cfg: Dict) -> Optional[str]:
    monthly_limit = plan_cfg.get("ai_monthly", 0)
    daily_limit = plan_cfg.get("ai_daily", 0)
    if monthly_limit >= 0 and user["plan_usage"].get("ai_month", 0) >= monthly_limit:
        return "AI monthly quota exceeded"
    if daily_limit >= 0 and user["plan_usage"].get("ai_day", 0) >= daily_limit:
        return "AI daily quota exceeded"
    return None


def check_voice_quota(user: Dict, plan_cfg: Dict) -> Optional[str]:
    monthly_limit = plan_cfg.get("voice_monthly", 0)
    if monthly_limit == 0:
        return "Voice input not available for your plan"
    if monthly_limit >= 0 and user["plan_usage"].get("voice_month", 0) >= monthly_limit:
        return "Voice monthly quota exceeded"
    return None


