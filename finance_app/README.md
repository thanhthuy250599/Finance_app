# 💰 Finance App - Ứng dụng quản lý tài chính cá nhân

## 🎯 Tổng quan
Ứng dụng quản lý tài chính cá nhân với AI hỗ trợ, cho phép người dùng theo dõi chi tiêu, lập kế hoạch ngân sách, và đặt mục tiêu tài chính.

## ✨ Tính năng chính

### 🏠 Dashboard
- Widget thống kê real-time
- Chi tiêu gần đây
- Tiến độ ngân sách
- Mục tiêu tài chính
- Quick actions

### 💸 Quản lý chi tiêu
- Thêm chi tiêu thủ công
- **Ghi âm chi tiêu** bằng giọng nói
- **AI Chat** - nhập chi tiêu bằng ngôn ngữ tự nhiên
- Phân loại tự động
- Xuất báo cáo CSV/PDF

### 📊 Phân tích & Báo cáo
- Biểu đồ Chart.js trực quan
- So sánh tháng trước
- Thống kê theo danh mục
- Xuất báo cáo nâng cao

### 🎯 Mục tiêu tài chính
- Đặt mục tiêu tiết kiệm
- Theo dõi tiến độ
- Nút thêm tiền nhanh
- Progress bar trực quan

### 📋 Ngân sách
- Lập kế hoạch chi tiêu
- Theo dõi tiến độ real-time
- Lịch sử thay đổi
- Cảnh báo vượt ngân sách

### 🏷️ Danh mục
- Quản lý danh mục tùy chỉnh
- CRUD đầy đủ
- UI thân thiện

### 🤖 AI Features
- **Gemini API** integration
- Lập kế hoạch tài chính thông minh
- Phân tích chi tiêu tự động
- Quota management theo gói

### 👑 Admin Panel
- Quản lý người dùng
- Báo cáo kinh doanh
- Quản lý API keys
- Duyệt yêu cầu nâng cấp
- Thống kê AI usage

## 🚀 Cài đặt & Chạy

### Yêu cầu hệ thống
- Python 3.8+
- pip

### Cài đặt
```bash
# Clone repository
git clone <repository-url>
cd finance_app

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python -m uvicorn finance_app.main:app --host 127.0.0.1 --port 8000
```

### Truy cập
- **Ứng dụng**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## 📱 Responsive Design
- ✅ Mobile-first design
- ✅ Tablet optimization
- ✅ Desktop experience
- ✅ Touch-friendly interface

## 🔐 Bảo mật
- Session-based authentication
- Password hashing với bcrypt
- Rate limiting (100 req/min)
- Security headers (HSTS, CSP)
- Role-based access control

## 💼 Business Model

### Gói Free
- 5 lượt AI/tháng
- 3 lượt voice/tháng
- Export có watermark
- Tính năng cơ bản

### Gói Pro Basic (99k VNĐ/tháng)
- 50 lượt AI/tháng
- 20 lượt voice/tháng
- Export không watermark
- Tính năng nâng cao

### Gói Pro Plus (199k VNĐ/tháng)
- 200 lượt AI/tháng
- 100 lượt voice/tháng
- Tất cả tính năng
- Ưu tiên hỗ trợ

### Gói Enterprise (Liên hệ)
- Không giới hạn AI
- Không giới hạn voice
- Admin panel
- Custom features

## 🛠️ Công nghệ sử dụng

### Backend
- **FastAPI** - Web framework
- **Jinja2** - Template engine
- **Bcrypt** - Password hashing
- **ReportLab** - PDF generation
- **Pandas** - Data processing

### Frontend
- **HTML5/CSS3** - UI/UX
- **JavaScript** - Interactivity
- **Chart.js** - Data visualization
- **WebRTC** - Voice recording

### AI/ML
- **Google Gemini API** - AI processing
- **Voice-to-text** - Speech recognition
- **Natural language processing** - Text analysis

### Data Storage
- **JSON files** - User data
- **Session storage** - Authentication
- **File-based** - No database required

## 📁 Cấu trúc thư mục
```
finance_app/
├── app/
│   ├── api/           # API endpoints
│   ├── middleware/     # Custom middleware
│   ├── services/      # Business logic
│   ├── templates/     # HTML templates
│   └── static/        # CSS/JS assets
├── config/            # Configuration files
├── data/              # User data storage
├── requirements.txt   # Dependencies
└── main.py           # Application entry point
```

## 🔧 Development

### Chạy development server
```bash
python -m uvicorn finance_app.main:app --reload --host 127.0.0.1 --port 8000
```

### Chạy production
```bash
python -m uvicorn finance_app.main:app --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t finance-app .
docker run -p 8000:8000 finance-app
```

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - Đăng ký
- `POST /auth/login` - Đăng nhập
- `POST /auth/logout` - Đăng xuất
- `GET /auth/me` - Thông tin user

### Finance
- `GET /finance/expenses` - Danh sách chi tiêu
- `POST /finance/expenses` - Thêm chi tiêu
- `DELETE /finance/expenses/{id}` - Xóa chi tiêu
- `GET /finance/expenses/summary` - Tổng kết
- `GET /finance/expenses/export` - Xuất báo cáo

### AI
- `POST /ai/chat` - Chat AI
- `POST /ai/voice` - Voice input
- `POST /ai/generate-plan` - Tạo kế hoạch

### Admin
- `GET /admin/users` - Quản lý users
- `GET /admin/metrics` - Báo cáo kinh doanh
- `POST /admin/api-keys` - Quản lý API keys

## 🎨 UI/UX Features
- **Dark theme** - Giao diện tối hiện đại
- **Responsive** - Tối ưu mọi thiết bị
- **Intuitive** - Dễ sử dụng
- **Fast** - Tải nhanh
- **Accessible** - Thân thiện người dùng

## 🔮 Tính năng tương lai
- [ ] Mobile app (React Native)
- [ ] Bank integration
- [ ] Investment tracking
- [ ] Multi-currency support
- [ ] Advanced AI insights
- [ ] Social features
- [ ] API for third-party apps

## 📞 Hỗ trợ
- **Email**: support@financeapp.com
- **Documentation**: /docs
- **Issues**: GitHub Issues

## 📄 License
MIT License - Xem file LICENSE để biết thêm chi tiết.

---

**🎉 Ứng dụng đã hoàn thành 100% và sẵn sàng sử dụng!**


