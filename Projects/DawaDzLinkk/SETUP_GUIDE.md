# 📚 DawaDzLink — Setup Guide

> Complete installation and configuration instructions

---

## Prerequisites

### Required Software
- **Git** — For cloning repositories
- **Node.js** (v18+) — For frontend development
- **Python 3.9+** — For backend API
- **Docker Desktop** — Recommended for deployment
- **MongoDB** — Local or cloud Atlas instance

---

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone <REPO_URL>
cd DawaDzLinkk
```

### 2. Start MongoDB Container

```bash
docker run -d -p 27017:27017 --name dawadzlink-mongo mongo:7
```

### 3. Start All Services

```bash
cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"
docker-compose up -d
```

### 4. Verify Containers

```bash
docker ps --filter "name=dawadzlink"
```

Expected output:
```
dawadzlink-mongodb   Up       MongoDB running
dawadzlink-backend   Up       API server on port 8001
dawadzlink-frontend  Up       Web app on port 3001
```

### 5. Access the Application

| Service | URL |
|---------|-----|
| Frontend Web App | http://127.0.0.1:3001 |
| Backend API | http://127.0.0.1:8001 |

---

## Python Development (No Docker)

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn motor bcrypt python-jwt python-dotenv email-validator sentry-sdk httpx
```

### 2. Create Environment File

Create `.env.local` in the `backend` directory:

```env
MONGO_URL=mongodb://localhost:27017/dawalink_local
DB_NAME=dawalink_local
JWT_SECRET=your-secret-key-here-should-be-long-and-random
```

### 3. Start Backend API

```bash
.\venv\Scripts\activate
uvicorn server:app --host 127.0.0.1 --port 8001
```

### 4. Setup Frontend

```bash
cd frontend
npm install
echo "VITE_REACT_APP_BACKEND_URL=http://localhost:8001" > .env
npm run dev
```

---

## Docker Commands Reference

### Rebuild Backend Only (After Code Changes)

```bash
cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"
python3 -m py_compile backend/server.py && echo "✅ Syntax OK"
docker-compose build backend --no-cache
docker-compose up -d backend
```

### Full Rebuild (If Container Crashes)

```bash
cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"
docker-compose down
docker rm -f dawadzlink-backend 2>/dev/null || true
docker-compose build backend --no-cache
docker-compose up -d backend
```

### Rebuild Everything

```bash
cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"
docker-compose build --no-cache
docker-compose up -d
```

---

## Testing the Registration Flow

### Test Pharmacy Registration (No Documents)

```bash
curl -X POST "http://localhost:8001/api/auth/register/pharmacy" ^
  -H "Content-Type: multipart/form-data" ^
  -F "email=pharm@example.dz" ^
  -F "password=securepass123" ^
  -F "full_name="Jean Dupont"" ^
  -F "phone="+336****0000" ^
  -F "pharmacy_name="Pharmacie Centrale"" ^
  -F "registry_number="REG12345" ^
  -F "address="123 Rue de la Paix" ^
  -F "wilaya="16"
```

### Test Supplier Registration (No Documents)

```bash
curl -X POST "http://localhost:8001/api/auth/register/supplier" ^
  -H "Content-Type: multipart/form-data" ^
  -F "email=fourn@example.dz" ^
  -F "password=securepass456" ^
  -F "full_name="Marie Martin"" ^
  -F "phone="+336****1111" ^
  -F "company_name="Distributeur Médical SAS"" ^
  -F "registry_number="COMP67890" ^
  -F "address="45 Avenue des Entreprises" ^
  -F "wilaya="31"
```

---

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongodb
```

Common issues:
- Port already in use — Check if port 8001 or 3001 is occupied
- MongoDB connection failed — Verify `.env.local` configuration
- Python syntax error — Run `python3 -m py_compile backend/server.py`

### Backend Rebuild After Code Changes

**NEVER blindly concatenate server.py files** — This silently deletes app initialization code and breaks containers!

Always verify before rebuilding:
```bash
python3 -m py_compile backend/server.py && echo "✅ Syntax OK"
```

### MongoDB Connection Issues

If using local MongoDB:
- Ensure MongoDB is running: `docker ps` or check system services
- Verify connection string in `.env.local`

---

## Production Deployment Checklist

- [ ] Set strong `JWT_SECRET` in production
- [ ] Use environment-specific MongoDB URL (production cluster)
- [ ] Enable Sentry for error tracking
- [ ] Configure CORS for production domain
- [ ] Review and approve all uploaded documents via admin panel
- [ ] Test email delivery for welcome emails

---

## 📖 Related Documentation

- [[DawaDzLink/README]] — Main project guide
- [[DawaDzLink/Changelog]] — Release notes
- [[Registration Flow]] — User authentication documentation

---

*Last updated: June 22, 2026*
