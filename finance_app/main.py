import os
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Response
from starlette.middleware.sessions import SessionMiddleware
from .app.api.utils import read_json, users_path
from .app.middleware.security import security_headers_middleware
from .app.middleware.rate_limit import rate_limit_middleware


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(key, default)
    return value


app = FastAPI(title="Finance App", version="0.1.0")

# Static & Templates
static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
templates_dir = os.path.join(os.path.dirname(__file__), "app", "templates")

if not os.path.isdir(static_dir):
    os.makedirs(static_dir, exist_ok=True)
if not os.path.isdir(templates_dir):
    os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_secret = get_env("SESSION_SECRET", "dev_secret_change_me")
app.add_middleware(SessionMiddleware, secret_key=session_secret)

# Extra middlewares
app.middleware("http")(security_headers_middleware)
app.middleware("http")(rate_limit_middleware(100))

# Routers
from .app.api.auth import router as auth_router  # noqa: E402
from .app.api.finance import router as finance_router  # noqa: E402
from .app.api.admin import router as admin_router  # noqa: E402
from .app.api.gemini import router as gemini_router  # noqa: E402
from .app.api.payment import router as payment_router  # noqa: E402
from .app.api.notification import router as notify_router  # noqa: E402
from .app.api.support import router as support_router  # noqa: E402

app.include_router(auth_router)
app.include_router(finance_router)
app.include_router(gemini_router)
app.include_router(payment_router)
app.include_router(notify_router)
app.include_router(support_router)
app.include_router(admin_router, prefix="/admin")
@app.get("/admin")
async def admin_index(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request})


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.get("/favicon.ico")
async def favicon():
    # Return a tiny 1x1 transparent PNG
    png_base64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
    )
    import base64
    data = base64.b64decode(png_base64)
    return Response(content=data, media_type="image/png")


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/upgrade")
async def upgrade_page(request: Request):
    return templates.TemplateResponse("upgrade.html", {"request": request})


@app.get("/generate-plan")
async def generate_plan_page(request: Request):
    return templates.TemplateResponse("generate-plan.html", {"request": request})


@app.get("/forgot-password")
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})


@app.get("/reset-password")
async def reset_password_page(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})


@app.get("/daily-chat-input")
async def daily_chat_input_page(request: Request):
    return templates.TemplateResponse("daily-chat-input.html", {"request": request})


@app.get("/analysis")
async def analysis_page(request: Request):
    return templates.TemplateResponse("analysis.html", {"request": request})


@app.get("/categories")
async def categories_page(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})


@app.get("/budget/edit")
async def budget_edit_page(request: Request):
    return templates.TemplateResponse("budget_edit.html", {"request": request})


@app.get("/expenses")
async def expenses_page(request: Request):
    return templates.TemplateResponse("expenses.html", {"request": request})


@app.get("/goals")
async def goals_page(request: Request):
    return templates.TemplateResponse("goals.html", {"request": request})


@app.get("/admin/users")
async def admin_users_page(request: Request):
    return templates.TemplateResponse("admin/users.html", {"request": request})


@app.get("/admin/api-keys")
async def admin_keys_page(request: Request):
    return templates.TemplateResponse("admin/api-keys.html", {"request": request})


@app.get("/admin/approve-upgrade")
async def admin_upgrade_page(request: Request):
    return templates.TemplateResponse("admin/approve-upgrade.html", {"request": request})


@app.get("/admin/metrics")
async def admin_metrics_page(request: Request):
    return templates.TemplateResponse("admin/metrics.html", {"request": request})


@app.get("/admin/support")
async def admin_support_page(request: Request):
    return templates.TemplateResponse("admin/support.html", {"request": request})


@app.get("/admin/notifications")
async def admin_notifications_page(request: Request):
    return templates.TemplateResponse("admin/notifications.html", {"request": request})


@app.get("/admin/bank-info")
async def admin_bank_info_page(request: Request):
    return templates.TemplateResponse("admin/bank-info.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)


