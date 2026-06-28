---
tags: []
aliases: []
created: 2026-06-27
---
# 🚀 DawaDzLink - Local Development Guide

> 💊 **Medication Distribution Platform** for Algeria  
> 🔗 Connecting Pharmacies, Suppliers & Healthcare Agents

---

## ✅ Quick Start

### Access URLs

| Service | Port/URL | Description |
|---------|----------|-------------|
| **Frontend Web App** | `http://127.0.0.1:3001` | Main web interface |
| **Backend API** | `http://127.0.0.1:8001` | REST API (for testing) |

---

## 🎯 Latest Features

### All Document Uploads Are Now OPTIONAL! 🎉

You can register as:
- **Pharmacy Owner** — No files needed at signup
- **Supplier** — No files needed at signup  
- **Agent** — No files needed at signup

Documents can be uploaded later via admin panel or Profile update.

---

## 📋 Docker Quick Start

```bash
# Start MongoDB
docker run -d -p 27017:27017 --name dawadzlink-mongo mongo:7

# Start all services
cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"
docker-compose up -d

# Verify containers are running
docker ps --filter "name=dawadzlink"
```

---

## 🐍 Python Development (No Docker)

### Prerequisites
1. Install MongoDB locally or use MongoDB Atlas
2. Activate virtual environment:
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install fastapi uvicorn motor bcrypt python-jwt python-dotenv email-validator sentry-sdk httpx
   ```

### Environment Setup
Create `.env.local` in backend:
```env
MONGO_URL=mongodb://localhost:27017@dawalink_local
DB_NAME=dawalink_local
JWT_SECRET=your-secret-key-here-should-be-long-and-random
```

### Run Backend API
```bash
uvicorn server:app --host 127.0.0.1 --port 8001
```

---

## 🧪 Test Endpoints

### Register Pharmacy (No Documents Required!)
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
  # agr_pharma_id and reg_commerce_id are optional!
```

### Register Supplier (No Documents Required!)
```bash
curl -X POST "http://localhost:8001/api/auth/register/supplier" ^
  -H "Content-Type: multipart/form-data" ^
  -F "email=fourn@example.dz" ^
  -F "password=securepass456" ^
  -F "full_name="Marie Martin"" ^
  -F "phone="+336****1111" ^
  -F "company_name="Distributeur Médical SAS"" ^
  -F "registry_number="COMP67890"
  # reg_com_id, agrément_id, fiscal_id are optional!
```

### Login & Get JWT Token
```bash
curl -X POST "http://localhost:8001/api/auth/login" ^
  -H "Content-Type: application/json" ^
  -d '{"email":"pharm@example.dz","password":"securepass123"}'
```

---

## 📂 Project Structure

```
DawaDzLinkk/
├── backend/              # FastAPI server (Python)
├── frontend/             # Vite React app
├── src/                  # Shared source code
├── memory/               # User data storage
├── docker-compose.yml    # Docker orchestration
└── .env.local*          # Environment configuration
```

---

## 🛠️ Development Workflow

### Rebuild Backend Only
```bash
cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"
python3 -m py_compile backend/server.py && echo "✅ Syntax OK"
docker-compose build backend --no-cache
docker-compose up -d backend
```

### Rebuild Everything
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔒 Security Notes

- ✅ Password hashing with bcrypt
- ✅ JWT authentication maintained
- ✅ CORS configured
- ⚠️ Document validation occurs if files provided
- ⚠️ Admin can review/approve accounts

---

## 📖 Additional Documentation

See related files:
- `DOCUMENTATION.md` — Complete development guide
- `RELEASE_NOTES.md` — Version history and changes
- `TROUBLESHOOTING.md` — Common issues and solutions

---

## 🚀 Status

**Current Version:** Latest with optional document uploads  
**Backend API:** `http://localhost:8001`  
**Frontend App:** `http://localhost:3001`  

All features operational! 🎉

---
#active-projects #dawadzlinkk #projects

