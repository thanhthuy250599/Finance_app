from fastapi import APIRouter, HTTPException, Depends, Request
import os
from ..api.utils import read_json, write_json, users_path

def require_admin(request: Request):
    session_user = request.session.get("user") if hasattr(request, "session") else None
    if not session_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    users = read_json(users_path(), [])
    u = next((x for x in users if x.get("username") == session_user.get("username")), None)
    if not u:
        raise HTTPException(status_code=401, detail="Authentication required")
    # Simple rule: admin if role==admin or plan==enterprise
    if u.get("role") == "admin" or u.get("plan") == "enterprise":
        return True
    raise HTTPException(status_code=403, detail="Admin only")


router = APIRouter(tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/admin/health")
async def admin_health():
    return {"admin": "ok"}


@router.get("/admin/users")
async def admin_users():
    users = read_json(users_path(), [])
    return {"users": users}


@router.get("/admin/api-keys")
async def admin_api_keys():
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "gemini_keys.json")
    return {"keys": read_json(cfg_path, [])}


@router.post("/admin/api-keys/add")
async def admin_api_keys_add(key: str, quota_limit: int = 100000):
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "gemini_keys.json")
    keys = read_json(cfg_path, [])
    if any(k.get("key") == key for k in keys):
        raise HTTPException(status_code=400, detail="Key exists")
    keys.append({"key": key, "quota_limit": quota_limit, "current_usage": 0, "last_used": None, "status": "active", "error_count": 0})
    write_json(cfg_path, keys)
    return {"ok": True}


@router.delete("/admin/api-keys/{key}")
async def admin_api_keys_delete(key: str):
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "gemini_keys.json")
    keys = read_json(cfg_path, [])
    new_list = [k for k in keys if k.get("key") != key]
    write_json(cfg_path, new_list)
    return {"ok": True}


@router.get("/admin/upgrade-requests")
async def admin_upgrade_requests():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "upgrade_requests.json")
    return {"items": read_json(path, [])}


@router.get("/admin/notifications-queue")
async def admin_notifications_queue():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "notifications_queue.json")
    return {"items": read_json(path, [])}


@router.post("/admin/approve-upgrade")
async def approve_upgrade(username: str, plan: str, approve: bool = True):
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    users = read_json(os.path.join(base, "data", "users.json"), [])
    reqs_path = os.path.join(base, "data", "upgrade_requests.json")
    reqs = read_json(reqs_path, [])
    # update request status
    for r in reqs:
        if r.get("username") == username and r.get("plan") == plan and r.get("status") == "pending":
            r["status"] = "approved" if approve else "rejected"
            break
    write_json(reqs_path, reqs)
    if approve:
        # update user plan
        for u in users:
            if u.get("username") == username:
                u["plan"] = plan
                break
        write_json(os.path.join(base, "data", "users.json"), users)
    return {"ok": True}


@router.get("/admin/bank-info")
async def admin_bank_info_get():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "bank_info.json")
    return read_json(path, {})


@router.post("/admin/bank-info")
async def admin_bank_info_set(account_name: str = "", account_number: str = "", bank: str = "", qr_base64: str = ""):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "bank_info.json")
    data = read_json(path, {})
    data.update({
        "account_name": account_name,
        "account_number": account_number,
        "bank": bank,
        "qr_base64": qr_base64,
    })
    write_json(path, data)
    return {"ok": True}


@router.get("/admin/metrics")
async def admin_metrics():
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    metrics_path = os.path.join(base, "business_metrics.json")
    users = read_json(os.path.join(base, "users.json"), [])
    upgrades = read_json(os.path.join(base, "upgrade_requests.json"), [])
    ai_log = read_json(os.path.join(base, "ai_call_log.json"), [])
    out = read_json(metrics_path, {})
    # simple aggregates
    out["total_users"] = len(users)
    out["upgrade_requests"] = len(upgrades)
    out["ai_calls_total"] = len(ai_log)
    out["pro_users"] = sum(1 for u in users if u.get("plan") in ("pro_basic", "pro_plus", "enterprise"))
    write_json(metrics_path, out)
    return out


