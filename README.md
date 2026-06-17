# Nepal National School Monitoring & Academic Intelligence Platform

**Government of Nepal — Ministry of Education, Science and Technology**

A centralized AI-powered education governance platform covering 35,000+ government schools, 250,000+ teachers, and millions of students across all 7 provinces.

---

## Quick Start

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local dev)
- MySQL 8.0+ (or use Docker)

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env — set DB credentials, AI API keys, etc.
```

### 3. Run with Docker
```bash
docker-compose up -d
# App: http://localhost
# API: http://localhost/api/v1/health
```

### 4. Run Locally (dev)
```bash
pip install -r requirements.txt
mysql -u root -p < schema.sql
flask db upgrade
flask run
```

---

## Project Structure
```
nepal_education_platform/
├── app/
│   ├── blueprints/          # auth, dashboard, schools, teachers, students, attendance, exams, api
│   ├── models/              # SQLAlchemy models
│   ├── services/            # AI, OCR, EMIS sync, TPDI engine, fraud detection
│   └── extensions.py        # Flask extensions
├── templates/               # Jinja2 HTML templates
│   ├── base.html            # Shared layout with sidebar
│   ├── auth/                # Login
│   ├── dashboard/           # Principal → Federal dashboards
│   ├── schools/             # School registry
│   ├── teachers/            # Teacher management
│   ├── attendance/          # GPS attendance & fraud alerts
│   └── exams/               # AI exam generation
├── static/css/style.css
├── static/js/main.js
├── schema.sql               # Full MySQL schema + Nepal province seed data
├── config.py                # Environment-based configuration
├── app.py                   # Entry point
├── Dockerfile
├── docker-compose.yml       # web + db + redis + celery + nginx
└── nginx.conf
```

---

## Phases Implemented

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Government School Registry + EMIS Sync | ✅ |
| 2 | Teacher Registry + GPS Attendance + Fraud Detection | ✅ |
| 3 | TPDI Performance Index Engine | ✅ |
| 4 | Student Academic Intelligence + Dropout Risk | ✅ |
| 5 | AI Exam Generation (OpenAI / Gemini) | ✅ |
| 6 | OCR Answer Sheet Evaluation (Tesseract + AI) | ✅ |
| 7 | Dashboards: Principal → Federal Ministry | ✅ |

---

## AI Configuration

Set `AI_PROVIDER` in `.env`:
- `openai` — uses GPT-4o (requires `OPENAI_API_KEY`)
- `gemini` — uses Gemini 1.5 Pro (requires `GEMINI_API_KEY`)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check (public) |
| GET | `/api/v1/schools` | List schools (JWT) |
| GET | `/api/v1/teachers` | List teachers (JWT) |
| GET | `/api/v1/students` | List students (JWT) |
| GET | `/api/v1/analytics/national` | National KPIs (JWT) |
| POST | `/attendance/checkin` | GPS check-in |
| POST | `/attendance/checkout` | GPS check-out |
| POST | `/exams/generate` | AI exam generation |
| POST | `/exams/evaluate-answersheet` | OCR evaluation |

---

## Default Login
- Username: `admin`
- **Change the password immediately after first login.**

---

*Built for Nepal's 35,000+ government schools — scalable to national deployment.*
