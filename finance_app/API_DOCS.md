# 📚 API Documentation - Finance App

## 🔗 Base URL
```
http://127.0.0.1:8000
```

## 🔐 Authentication

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "referral_code": "optional_referral_code"
}
```

**Response:**
```json
{
  "ok": true,
  "message": "User registered successfully",
  "user": {
    "username": "john_doe",
    "plan": "free",
    "points": 0
  }
}
```

### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "ok": true,
  "message": "Login successful",
  "user": {
    "username": "john_doe",
    "plan": "free",
    "points": 0
  }
}
```

### Get Current User
```http
GET /auth/me
```

**Response:**
```json
{
  "authenticated": true,
  "username": "john_doe",
  "plan": "free",
  "points": 0,
  "role": "user"
}
```

### Logout
```http
POST /auth/logout
```

## 💰 Finance Management

### Get Expenses
```http
GET /finance/expenses?username=john_doe
```

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "category": "Ăn uống",
    "amount": 50000,
    "note": "Cơm trưa"
  }
]
```

### Add Expense
```http
POST /finance/expenses
Content-Type: application/json

{
  "date": "2024-01-15",
  "category": "Ăn uống",
  "amount": 50000,
  "note": "Cơm trưa"
}
```

### Delete Expense
```http
DELETE /finance/expenses/{index}
```

### Get Expenses Summary
```http
GET /finance/expenses/summary?username=john_doe
```

**Response:**
```json
{
  "month": "2024-01",
  "total": 1500000,
  "by_category": {
    "Ăn uống": 500000,
    "Di chuyển": 300000,
    "Mua sắm": 700000
  },
  "count": 15
}
```

### Compare Month
```http
GET /finance/expenses/compare-month?username=john_doe
```

**Response:**
```json
{
  "current": {
    "month": "2024-01",
    "total": 1500000,
    "count": 15
  },
  "previous": {
    "month": "2023-12",
    "total": 1200000,
    "count": 12
  },
  "delta": 300000,
  "percent": 25.0
}
```

### Export Expenses
```http
GET /finance/expenses/export?format=csv&username=john_doe
GET /finance/expenses/export?format=pdf&username=john_doe
```

## 🎯 Goals Management

### Get Goals
```http
GET /finance/goals?username=john_doe
```

**Response:**
```json
{
  "items": [
    {
      "title": "Tiết kiệm mua xe",
      "target_amount": 10000000,
      "due_months": 12,
      "saved_amount": 2000000
    }
  ]
}
```

### Add Goal
```http
POST /finance/goals
Content-Type: application/json

{
  "title": "Tiết kiệm mua xe",
  "target_amount": 10000000,
  "due_months": 12,
  "saved_amount": 0
}
```

### Update Goal Progress
```http
POST /finance/goals/{index}/progress?amount=500000
```

## 📋 Budget Management

### Get Budget
```http
GET /finance/budget?username=john_doe
```

**Response:**
```json
{
  "items": [
    {
      "name": "Ăn uống",
      "amount": 500000
    },
    {
      "name": "Di chuyển",
      "amount": 300000
    }
  ]
}
```

### Save Budget
```http
POST /finance/budget
Content-Type: application/json

{
  "items": [
    {
      "name": "Ăn uống",
      "amount": 500000
    }
  ],
  "version_note": "Cập nhật ngân sách tháng 1"
}
```

### Get Budget History
```http
GET /finance/budget/history?username=john_doe
```

## 🏷️ Categories Management

### Get Categories
```http
GET /finance/categories?username=john_doe
```

**Response:**
```json
{
  "items": [
    {"name": "Ăn uống"},
    {"name": "Di chuyển"},
    {"name": "Mua sắm"}
  ]
}
```

### Add Category
```http
POST /finance/categories
Content-Type: application/json

{
  "name": "Giải trí"
}
```

### Delete Category
```http
DELETE /finance/categories/{name}
```

## 🤖 AI Features

### Chat Input
```http
POST /ai/chat
Content-Type: application/json

{
  "text": "ăn cơm 30k, mua áo 150k"
}
```

**Response:**
```json
{
  "ok": true,
  "expenses": [
    {
      "date": "2024-01-15",
      "category": "Ăn uống",
      "amount": 30000,
      "note": "ăn cơm 30k"
    },
    {
      "date": "2024-01-15",
      "category": "Mua sắm",
      "amount": 150000,
      "note": "mua áo 150k"
    }
  ]
}
```

### Voice Input
```http
POST /ai/voice
Content-Type: audio/wav

[Audio file binary data]
```

**Response:**
```json
{
  "ok": true,
  "text": "ăn cơm 30k"
}
```

### Generate Financial Plan
```http
POST /ai/generate-plan
Content-Type: application/json

{
  "income": 10000000,
  "goals": ["Mua xe", "Tiết kiệm khẩn cấp"]
}
```

### Get Chat History
```http
GET /ai/chat/history?username=john_doe
```

## 🔔 Notifications

### Get Notifications
```http
GET /notifications?username=john_doe
```

**Response:**
```json
[
  {
    "id": "notif_1",
    "title": "Chào mừng!",
    "message": "Chào mừng bạn đến với Finance App",
    "timestamp": "2024-01-15T10:30:00Z",
    "read": false
  }
]
```

### Mark as Read
```http
POST /notifications/{notification_id}/read
```

## 💳 Payment & Upgrade

### Apply Promo Code
```http
POST /payment/promo
Content-Type: application/json

{
  "code": "WELCOME2024"
}
```

### Request Upgrade
```http
POST /payment/upgrade
Content-Type: application/json

{
  "plan": "pro_basic",
  "payment_method": "bank_transfer",
  "notes": "Nâng cấp lên Pro Basic"
}
```

## 👑 Admin APIs

### Get Users (Admin only)
```http
GET /admin/users
```

**Response:**
```json
{
  "users": [
    {
      "username": "john_doe",
      "email": "john@example.com",
      "plan": "free",
      "points": 0,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Business Metrics
```http
GET /admin/metrics?start_date=2024-01-01&end_date=2024-01-31
```

**Response:**
```json
{
  "total_users": 150,
  "new_users": 25,
  "active_users": 120,
  "conversion_rate": 15.5,
  "total_revenue": 5000000,
  "ai_calls": 1250,
  "plan_distribution": {
    "free": 100,
    "pro_basic": 30,
    "pro_plus": 15,
    "enterprise": 5
  }
}
```

### Manage API Keys
```http
# Get API Keys
GET /admin/api-keys

# Add API Key
POST /admin/api-keys
Content-Type: application/json
{
  "key": "your-gemini-api-key",
  "name": "Production Key"
}

# Delete API Key
DELETE /admin/api-keys/{key_id}
```

### Approve Upgrade Requests
```http
POST /admin/upgrade-requests/{request_id}/approve
```

## 📊 Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## 🔧 Rate Limits

- **General API**: 100 requests/minute per IP
- **AI Features**: Based on user plan
  - Free: 5 AI calls/month, 3 voice calls/month
  - Pro Basic: 50 AI calls/month, 20 voice calls/month
  - Pro Plus: 200 AI calls/month, 100 voice calls/month
  - Enterprise: Unlimited

## 📝 Request/Response Examples

### Complete Expense Workflow
```bash
# 1. Register user
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","email":"test@example.com","password":"password123"}'

# 2. Add expense
curl -X POST http://127.0.0.1:8000/finance/expenses \
  -H "Content-Type: application/json" \
  -d '{"date":"2024-01-15","category":"Ăn uống","amount":50000,"note":"Cơm trưa"}'

# 3. Get summary
curl -X GET http://127.0.0.1:8000/finance/expenses/summary?username=test_user

# 4. Export CSV
curl -X GET http://127.0.0.1:8000/finance/expenses/export?format=csv&username=test_user
```

### AI Chat Workflow
```bash
# 1. Chat input
curl -X POST http://127.0.0.1:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"ăn cơm 30k, mua áo 150k"}'

# 2. Get chat history
curl -X GET http://127.0.0.1:8000/ai/chat/history?username=test_user
```

## 🚀 Interactive API Documentation

Truy cập **Swagger UI** tại: http://127.0.0.1:8000/docs

Truy cập **ReDoc** tại: http://127.0.0.1:8000/redoc

---

**📚 API Documentation hoàn chỉnh - Sẵn sàng sử dụng!**


