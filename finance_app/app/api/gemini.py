from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from .utils import read_json, write_json, users_path
from .ai_limit import (
    get_plan_limits,
    should_reset_month,
    log_ai_call,
    log_reset,
    ensure_usage_fields,
    reset_month_if_needed,
    reset_day_if_needed,
    check_ai_quota,
)
from typing import Optional
from datetime import datetime
from ..services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


class PlanRequest(BaseModel):
    income: float
    goals: List[str] = []


@router.post("/generate-plan")
async def generate_plan(req: PlanRequest):
    # Simplified: assume single demo user for now
    username = "demo"
    users = read_json(users_path(), [])
    user = next((u for u in users if u.get("username") == username), None)
    if not user:
        user = {"username": username, "plan": "free", "plan_usage": {"ai_month": 0, "ai_day": 0}, "last_reset_month": None}
        users.append(user)

    ensure_usage_fields(user)
    reset_month_if_needed(user, username)
    reset_day_if_needed(user, username)

    limits = get_plan_limits(user.get("plan", "free"))
    quota_error = check_ai_quota(user, limits)
    if quota_error:
        raise HTTPException(status_code=429, detail=quota_error)

    try:
        service = AIService()
        mock_plan = service.generate_plan(req.income, req.goals)
    except Exception as e:
        log_ai_call({"username": username, "type": "generate_plan", "ts": datetime.utcnow().isoformat(), "status": "error", "error": str(e)})
        raise HTTPException(status_code=502, detail="AI service temporarily unavailable")
    # increment usage and log
    user["plan_usage"]["ai_month"] = user["plan_usage"].get("ai_month", 0) + 1
    user["plan_usage"]["ai_day"] = user["plan_usage"].get("ai_day", 0) + 1
    write_json(users_path(), users)
    log_ai_call({"username": username, "type": "generate_plan", "ts": datetime.utcnow().isoformat(), "status": "ok"})
    return {"ok": True, "plan": mock_plan}


class VoiceInputRequest(BaseModel):
    audio_base64: str


@router.post("/voice-input")
async def voice_input(_: VoiceInputRequest):
    # Quota check for voice
    username = "demo"
    users = read_json(users_path(), [])
    user = next((u for u in users if u.get("username") == username), None)
    if not user:
        user = {"username": username, "plan": "free", "plan_usage": {"ai_month": 0, "ai_day": 0, "voice_month": 0}, "last_reset_month": None}
        users.append(user)
    ensure_usage_fields(user)
    reset_month_if_needed(user, username)
    limits = get_plan_limits(user.get("plan", "free"))
    # Free/Pro Basic -> voice not allowed
    voice_limit = limits.get("voice_monthly", 0)
    if voice_limit == 0:
        raise HTTPException(status_code=403, detail="Voice input not available for your plan")
    if voice_limit > 0 and user["plan_usage"]["voice_month"] >= voice_limit:
        raise HTTPException(status_code=429, detail="Voice monthly quota exceeded")
    # Stub transcription
    user["plan_usage"]["voice_month"] += 1
    write_json(users_path(), users)
    return {"ok": True, "text": "ăn cơm 30k"}


class ChatRequest(BaseModel):
    text: str


@router.post("/chat")
async def chat_parse(req: ChatRequest, username: str = "demo"):
    # Check AI quota first
    if not check_ai_quota(username):
        return {"ok": False, "message": "Đã hết quota AI cho tháng này. Vui lòng nâng cấp để tiếp tục sử dụng."}
    
    # Enhanced parser: split by commas, extract trailing numbers as amounts
    items = []
    for part in req.text.split(','):
        seg = part.strip()
        if not seg:
            continue
        tokens = seg.split()
        amount = None
        category = "Khác"
        
        # Determine category based on keywords
        seg_lower = seg.lower()
        if any(word in seg_lower for word in ['ăn', 'cơm', 'trà', 'nước', 'cafe', 'bánh']):
            category = "Ăn uống"
        elif any(word in seg_lower for word in ['mua', 'áo', 'quần', 'giày', 'túi']):
            category = "Mua sắm"
        elif any(word in seg_lower for word in ['xăng', 'đổ', 'xe', 'taxi', 'grab']):
            category = "Di chuyển"
        elif any(word in seg_lower for word in ['phim', 'game', 'giải trí', 'karaoke']):
            category = "Giải trí"
        elif any(word in seg_lower for word in ['thuốc', 'bệnh viện', 'y tế', 'khám']):
            category = "Y tế"
        elif any(word in seg_lower for word in ['học', 'sách', 'khóa học', 'trường']):
            category = "Học tập"
        
        for t in reversed(tokens):
            t_clean = t.lower().replace('k', '000').replace('.', '').replace(',', '')
            if t_clean.isdigit():
                amount = float(t_clean)
                break
        label = seg
        items.append({"label": label, "amount": amount, "category": category})
    
    # Save parsed chat as expenses
    from .finance import add_expense, Expense  # local import to avoid cycle at module load
    saved = []
    for it in items:
        if it.get("amount"):
            exp = Expense(
                date=datetime.utcnow().strftime("%Y-%m-%d"), 
                category=it["category"], 
                amount=it["amount"], 
                note=it["label"]
            ) 
            await add_expense(exp, username)
            saved.append(exp.dict())
    
    # Log AI call
    log_ai_call(username, "chat_parse")
    
    # Save to chat history
    history_path = os.path.join(user_data_dir(username), "chat_history.json")
    history = read_json(history_path, [])
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "input": req.text,
        "expenses": saved
    })
    write_json(history_path, history)
    
    return {"ok": True, "expenses": saved}


@router.get("/chat/history")
async def get_chat_history(username: str = "demo"):
    history_path = os.path.join(user_data_dir(username), "chat_history.json")
    history = read_json(history_path, [])
    return history[-20:]  # Return last 20 entries


