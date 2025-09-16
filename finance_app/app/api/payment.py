from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from .utils import read_json, write_json
import os

router = APIRouter(prefix="/payment", tags=["payment"])


def _promo_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "promo_codes.json")


class UpgradeRequest(BaseModel):
    plan: str
    promo: Optional[str] = None
    amount_vnd: int


@router.post("/apply-promo")
async def apply_promo(code: str):
    codes = read_json(_promo_path(), {})
    promo = codes.get(code.upper())
    if not promo or not promo.get("active"):
        return {"ok": False, "message": "invalid"}
    return {"ok": True, "discount_percent": promo.get("discount_percent", 0)}


@router.post("/request-upgrade")
async def request_upgrade(req: UpgradeRequest, request: Request):
    # Stub: record request for admin approval
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "upgrade_requests.json")
    data = read_json(path, [])
    username = (request.session.get("user") or {}).get("username", "demo")
    data.append({"username": username, "plan": req.plan, "promo": req.promo, "amount_vnd": req.amount_vnd, "status": "pending"})
    write_json(path, data)
    return {"ok": True}


