from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from datetime import datetime, timedelta
from .utils import read_json, write_json, user_data_dir
import io
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from collections import defaultdict

router = APIRouter(prefix="/finance", tags=["finance"])


class Expense(BaseModel):
    date: str
    category: str
    amount: float
    note: Optional[str] = None


@router.get("/expenses", response_model=List[Expense])
async def list_expenses(username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(user_data_dir(username), f"expenses_{year_month}.json")
    data = read_json(path, [])
    return data


@router.post("/expenses")
async def add_expense(expense: Expense, username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(user_data_dir(username), f"expenses_{year_month}.json")
    data = read_json(path, [])
    data.insert(0, expense.dict())
    write_json(path, data)
    return {"ok": True, "expense": expense}


@router.delete("/expenses/{index}")
async def delete_expense(index: int, username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(user_data_dir(username), f"expenses_{year_month}.json")
    data = read_json(path, [])
    if 0 <= index < len(data):
        data.pop(index)
        write_json(path, data)
        return {"ok": True}
    raise HTTPException(status_code=404, detail="Not found")


@router.get("/budget")
async def get_budget(username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(user_data_dir(username), f"budget_{year_month}.json")
    data = read_json(path, {"items": []})
    return data


@router.get("/expenses/export")
async def export_expenses(format: str = "csv", username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(user_data_dir(username), f"expenses_{year_month}.json")
    data: List[dict] = read_json(path, [])
    if format == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=["date", "category", "amount", "note"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return Response(content=buf.getvalue(), media_type="text/csv")
    elif format == "pdf":
        buf = io.BytesIO()
        pdf = canvas.Canvas(buf, pagesize=A4)
        textobject = pdf.beginText(40, 800)
        textobject.textLine(f"Expenses {year_month} for {username}")
        textobject.textLine("")
        for row in data[:200]:
            line = f"{row.get('date')} | {row.get('category')} | {row.get('amount')} | {row.get('note','')}"
            textobject.textLine(line)
        pdf.drawText(textobject)
        pdf.showPage()
        pdf.save()
        return Response(content=buf.getvalue(), media_type="application/pdf")
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")


@router.get("/expenses/summary")
async def expenses_summary(username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(user_data_dir(username), f"expenses_{year_month}.json")
    data: List[dict] = read_json(path, [])
    total = 0.0
    by_cat: Dict[str, float] = defaultdict(float)
    for row in data:
        amt = float(row.get("amount", 0) or 0)
        total += amt
        by_cat[row.get("category", "Other")] += amt
    return {"month": year_month, "total": total, "by_category": by_cat, "count": len(data)}


@router.get("/expenses/compare-month")
async def compare_month(username: str = "demo"):
    now = datetime.utcnow()
    curr_key = now.strftime("%Y-%m")
    prev_month = (now.replace(day=1) - timedelta(days=1))
    prev_key = prev_month.strftime("%Y-%m")
    curr_path = os.path.join(user_data_dir(username), f"expenses_{curr_key}.json")
    prev_path = os.path.join(user_data_dir(username), f"expenses_{prev_key}.json")
    curr = read_json(curr_path, [])
    prev = read_json(prev_path, [])
    def total(items):
        return float(sum(float(x.get("amount", 0) or 0) for x in items))
    curr_total = total(curr)
    prev_total = total(prev)
    delta = curr_total - prev_total
    pct = (delta / prev_total * 100) if prev_total else None
    return {"current": {"month": curr_key, "total": curr_total, "count": len(curr)},
            "previous": {"month": prev_key, "total": prev_total, "count": len(prev)},
            "delta": delta, "percent": pct}


class ReceiptOCRRequest(BaseModel):
    image_base64: Optional[str] = None


@router.post("/receipt-ocr")
async def receipt_ocr(_: ReceiptOCRRequest):
    # Stub: return a fixed example
    return {"ok": True, "items": [{"label": "Cafe", "amount": 25000}]}


class Goal(BaseModel):
    title: str
    target_amount: float
    due_months: int
    saved_amount: float = 0


@router.get("/goals")
async def list_goals(username: str = "demo"):
    path = os.path.join(user_data_dir(username), "goals.json")
    return read_json(path, {"items": []})


@router.post("/goals")
async def add_goal(goal: Goal, username: str = "demo"):
    path = os.path.join(user_data_dir(username), "goals.json")
    data = read_json(path, {"items": []})
    data["items"].append(goal.dict())
    write_json(path, data)
    return {"ok": True}


@router.post("/goals/{index}/progress")
async def update_goal_progress(index: int, amount: float, username: str = "demo"):
    path = os.path.join(user_data_dir(username), "goals.json")
    data = read_json(path, {"items": []})
    if index < 0 or index >= len(data.get("items", [])):
        raise HTTPException(status_code=404, detail="Goal not found")
    data["items"][index]["saved_amount"] = float(data["items"][index].get("saved_amount", 0)) + float(amount)
    write_json(path, data)
    return {"ok": True}


class CategoryIn(BaseModel):
    name: str


@router.get("/categories")
async def list_categories(username: str = "demo"):
    path = os.path.join(user_data_dir(username), "categories.json")
    data = read_json(path, {"items": []})
    return data


@router.post("/categories")
async def add_category(cat: CategoryIn, username: str = "demo"):
    path = os.path.join(user_data_dir(username), "categories.json")
    data = read_json(path, {"items": []})
    items = data.get("items", [])
    if any(i.get("name") == cat.name for i in items):
        return {"ok": False, "message": "exists"}
    items.append({"name": cat.name})
    data["items"] = items
    write_json(path, data)
    return {"ok": True}


@router.delete("/categories/{name}")
async def delete_category(name: str, username: str = "demo"):
    path = os.path.join(user_data_dir(username), "categories.json")
    data = read_json(path, {"items": []})
    items = [i for i in data.get("items", []) if i.get("name") != name]
    data["items"] = items
    write_json(path, data)
    return {"ok": True}


class BudgetItem(BaseModel):
    name: str
    amount: float


class BudgetPayload(BaseModel):
    items: List[BudgetItem]
    version_note: Optional[str] = None


@router.post("/budget")
async def save_budget(payload: BudgetPayload, username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    dir_path = user_data_dir(username)
    path = os.path.join(dir_path, f"budget_{year_month}.json")
    history_path = os.path.join(dir_path, f"budget_{year_month}_history.json")
    current = read_json(path, {"items": []})
    history = read_json(history_path, [])
    # append current to history with timestamp
    history.append({
        "ts": datetime.utcnow().isoformat(),
        "data": current,
        "note": payload.version_note or ""
    })
    write_json(history_path, history)
    write_json(path, {"items": [i.dict() for i in payload.items]})
    return {"ok": True}


@router.get("/budget/history")
async def get_budget_history(username: str = "demo"):
    year_month = datetime.utcnow().strftime("%Y-%m")
    history_path = os.path.join(user_data_dir(username), f"budget_{year_month}_history.json")
    history = read_json(history_path, [])
    return history


