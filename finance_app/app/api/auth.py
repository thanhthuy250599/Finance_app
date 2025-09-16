from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.hash import bcrypt
from .utils import read_json, write_json, users_path
import os, secrets
from datetime import datetime, timedelta
from ..services.email_service import EmailService

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    referral_code: Optional[str] = None


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


@router.post("/register")
async def register_user(body: RegisterRequest):
    users = read_json(users_path(), [])
    if any(u.get("username") == body.username or u.get("email") == body.email for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    user = {
        "username": body.username,
        "email": str(body.email),
        "password_hash": bcrypt.hash(body.password),
        "plan": "free",
        "plan_usage": {"ai_month": 0, "ai_day": 0, "voice_month": 0},
        "last_reset_day": None,
        "last_reset_month": None,
        "timezone": "Asia/Ho_Chi_Minh",
        "referral_code": body.referral_code or None,
        "points": 0,
    }
    # Referral bonus: if referral_code matches an existing username, give both 1 month-equivalent points (stub: +50)
    if body.referral_code:
        ref = next((u for u in users if u.get("username") == body.referral_code), None)
        if ref:
            ref["points"] = int(ref.get("points", 0)) + 50
            user["points"] = int(user.get("points", 0)) + 50
    users.append(user)
    write_json(users_path(), users)
    return {"ok": True, "message": "registered", "user": {"username": body.username, "email": body.email}}


@router.post("/login")
async def login_user(body: LoginRequest):
    users = read_json(users_path(), [])
    user = next((u for u in users if u.get("username") == body.username_or_email or u.get("email") == body.username_or_email), None)
    if not user or not bcrypt.verify(body.password, user.get("password_hash", "")):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"ok": True, "message": "logged_in", "user": {"username": user["username"], "plan": user.get("plan", "free")}}


@router.post("/login-form")
async def login_form(request: Request, username_or_email: str = Form(...), password: str = Form(...)):
    users = read_json(users_path(), [])
    user = next((u for u in users if u.get("username") == username_or_email or u.get("email") == username_or_email), None)
    if not user or not bcrypt.verify(password, user.get("password_hash", "")):
        response = RedirectResponse(url="/login?error=1", status_code=302)
        return response
    request.session["user"] = {"username": user["username"], "plan": user.get("plan", "free"), "role": user.get("role", "user")}
    return RedirectResponse(url="/", status_code=302)


@router.post("/register-form")
async def register_form(request: Request, username: str = Form(...), email: EmailStr = Form(...), password: str = Form(...), referral_code: str = Form(None)):
    users = read_json(users_path(), [])
    if any(u.get("username") == username or u.get("email") == str(email) for u in users):
        return RedirectResponse(url="/register?error=1", status_code=302)
    user = {
        "username": username,
        "email": str(email),
        "password_hash": bcrypt.hash(password),
        "plan": "free",
        "plan_usage": {"ai_month": 0, "ai_day": 0, "voice_month": 0},
        "last_reset_day": None,
        "last_reset_month": None,
        "timezone": "Asia/Ho_Chi_Minh",
        "referral_code": referral_code or None,
        "points": 0,
        "role": "user",
    }
    if referral_code:
        ref = next((u for u in users if u.get("username") == referral_code), None)
        if ref:
            ref["points"] = int(ref.get("points", 0)) + 50
            user["points"] = int(user.get("points", 0)) + 50
    users.append(user)
    write_json(users_path(), users)
    request.session["user"] = {"username": username, "plan": "free", "role": "user"}
    return RedirectResponse(url="/", status_code=302)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)


@router.get("/me")
async def me(request: Request):
    user_session = request.session.get("user")
    if not user_session:
        return {"authenticated": False}
    users = read_json(users_path(), [])
    user = next((u for u in users if u.get("username") == user_session.get("username")), None)
    if not user:
        return {"authenticated": False}
    return {
        "authenticated": True,
        "username": user.get("username"),
        "plan": user.get("plan", "free"),
        "points": user.get("points", 0)
    }


@router.post("/forgot-password")
async def forgot_password(email: EmailStr):
    users = read_json(users_path(), [])
    user = next((u for u in users if u.get("email") == str(email)), None)
    token_store = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "password_resets.json")
    resets = read_json(token_store, [])
    if user:
        token = secrets.token_urlsafe(24)
        resets.append({
            "username": user["username"],
            "token": token,
            "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat()
        })
        write_json(token_store, resets)
        EmailService().send(str(email), "Password Reset", f"Use this token to reset: {token}")
    return {"ok": True}


@router.post("/forgot-password-form")
async def forgot_password_form(email: EmailStr = Form(...)):
    await forgot_password(email)
    return RedirectResponse(url="/reset-password", status_code=302)


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


@router.post("/reset-password")
async def reset_password(body: ResetPasswordRequest):
    token_store = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "password_resets.json")
    resets = read_json(token_store, [])
    now = datetime.utcnow()
    record = next((r for r in resets if r.get("token") == body.token), None)
    if not record:
        raise HTTPException(status_code=400, detail="Invalid token")
    if datetime.fromisoformat(record.get("expires_at")) < now:
        raise HTTPException(status_code=400, detail="Token expired")
    users = read_json(users_path(), [])
    for u in users:
        if u.get("username") == record.get("username"):
            u["password_hash"] = bcrypt.hash(body.new_password)
            break
    write_json(users_path(), users)
    resets = [r for r in resets if r.get("token") != body.token]
    write_json(token_store, resets)
    return {"ok": True}


