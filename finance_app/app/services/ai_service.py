from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, List
import os
import time
from ..api.utils import read_json, write_json


@dataclass
class GeminiKey:
    key: str
    quota_limit: int
    current_usage: int
    last_used: Optional[str]
    status: str
    error_count: int


class AIService:
    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        self.model_name = model_name

    def _keys_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "gemini_keys.json")

    def _load_keys(self) -> List[Dict[str, Any]]:
        return read_json(self._keys_path(), [])

    def _save_keys(self, keys: List[Dict[str, Any]]) -> None:
        write_json(self._keys_path(), keys)

    def choose_key(self) -> Optional[GeminiKey]:
        keys = self._load_keys()
        now = time.time()
        eligible = []
        for k in keys:
            disabled_until = k.get("last_disabled_until")
            if disabled_until and now < float(disabled_until):
                continue
            if k.get("status", "active") != "active":
                continue
            eligible.append(k)
        if not eligible:
            return None
        # pick least used
        eligible.sort(key=lambda x: (x.get("current_usage", 0), x.get("last_used") or ""))
        k = eligible[0]
        return GeminiKey(
            key=k.get("key", ""),
            quota_limit=int(k.get("quota_limit", 0)),
            current_usage=int(k.get("current_usage", 0)),
            last_used=k.get("last_used"),
            status=k.get("status", "active"),
            error_count=int(k.get("error_count", 0)),
        )

    def _update_key_after_call(self, chosen_key: Optional[GeminiKey], success: bool) -> None:
        if not chosen_key:
            return
        keys = self._load_keys()
        changed = False
        now = time.time()
        for k in keys:
            if k.get("key") == chosen_key.key:
                if success:
                    k["current_usage"] = int(k.get("current_usage", 0)) + 1
                    k["error_count"] = 0
                    k["last_used"] = now
                else:
                    k["error_count"] = int(k.get("error_count", 0)) + 1
                    if k["error_count"] >= 3:
                        k["status"] = "disabled"
                        k["last_disabled_until"] = now + 300  # 5 minutes
                changed = True
                break
        if changed:
            self._save_keys(keys)

    def generate_plan(self, income: float, goals: List[str]) -> Dict[str, Any]:
        # In real implementation, call Gemini with retries/backoff.
        chosen = self.choose_key()
        try:
            # MOCK response
            result = {
                "savings": round(income * 0.2, 2),
                "food": round(income * 0.25, 2),
                "transport": round(income * 0.1, 2),
                "others": round(income * 0.45, 2),
                "goals": goals,
                "_using_key": chosen.key if chosen else None,
            }
            self._update_key_after_call(chosen, True)
            return result
        except Exception:
            self._update_key_after_call(chosen, False)
            raise


