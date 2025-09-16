from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from .utils import read_json, write_json

router = APIRouter(prefix="/notify", tags=["notify"])


def _queue_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "notifications_queue.json")


class NotifyRequest(BaseModel):
    kind: str  # email|in_app
    to: Optional[EmailStr] = None
    message: str


@router.post("/enqueue")
async def enqueue_notify(req: NotifyRequest):
    q = read_json(_queue_path(), [])
    q.append(req.dict())
    write_json(_queue_path(), q)
    return {"ok": True, "queued": True}






