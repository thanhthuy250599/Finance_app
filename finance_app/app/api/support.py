from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import os
from .utils import read_json, write_json

router = APIRouter(prefix="/support", tags=["support"])


def _tickets_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "support_tickets.json")


class Ticket(BaseModel):
    subject: str
    message: str
    priority: str = "normal"


@router.get("/tickets")
async def list_tickets():
    return {"items": read_json(_tickets_path(), [])}


@router.post("/tickets")
async def create_ticket(t: Ticket):
    items = read_json(_tickets_path(), [])
    items.append({"subject": t.subject, "message": t.message, "priority": t.priority, "status": "open"})
    write_json(_tickets_path(), items)
    return {"ok": True}






