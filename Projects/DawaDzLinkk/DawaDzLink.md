# 🧭 DawaDzLink — Project Reference

> **Main Documentation Hub** for the DawaDzLinkk project

---

## Overview

This repository contains a medication distribution platform designed to connect pharmacies, suppliers, and healthcare agents across Algeria. The latest version features optional document uploads during registration.

### Key Features
- ✅ User registration without mandatory document uploads
- ✅ Document upload capability (optional) for pharmacy/supplier verification
- ✅ Multi-role access: Pharmacies, Suppliers, Agents
- ✅ Docker-based deployment with MongoDB

---

## 📂 Documentation Structure

| File | Purpose | Link |
|------|---------|------|
| `README.md` | Main project guide and quick start | [[DawaDzLink/README]] |
| `CHANGELOG.md` | Release notes and version history | [[DawaDzLink/Changelog]] |
| `SETUP_GUIDE.md` | Detailed setup instructions (coming soon) | [[DawaDzLink/Setup-Guide]] |

---

## 🚀 Quick Start

1. **Start MongoDB:**
   ```bash
   docker run -d -p 27017:27017 --name dawadzlink-mongo mongo:7
   ```

2. **Start all services:**
   ```bash
   cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"
   docker-compose up -d
   ```

3. **Access the app:**
   - Frontend: `http://127.0.0.1:3001`
   - Backend API: `http://127.0.0.1:8001`

---

## 🎯 Latest Update — Optional Document Uploads (June 22, 2026)

### Summary
All document uploads are now **completely optional** during registration for both suppliers and pharmacies. Users can create accounts immediately after providing basic information:
- Name
- Email
- Phone
- Address
- Password

Document uploads can be added later via admin panel or profile updates.

### Affected User Types

#### Suppliers — All Documents Optional
| Document | Status | Description |
|----------|--------|-------------|
| Registre de commerce | ✅ Optional | Trade Register |
| Agrément | ✅ Optional | Commercial License |
| Certificat fiscal | ✅ Optional | Tax Certificate |

#### Pharmacies — All Documents Optional
| Document | Status | Description |
|----------|--------|-------------|
| Agrément de pharmacie | ✅ Optional | Pharmacy License |
| Registre de Commerce | ✅ Optional | Trade Register |
| Inscription à l'ordre des pharmaciens | ✅ Optional | Pharmacy Order Registration |

---

## 🔗 Related Documentation in Vault

- [[Projects]] — All projects hub
- [[DawaDzLink/README]] — Main project documentation
- [[DawaDzLink/Changelog]] — Version history and release notes
- [[Registration Flow]] — User authentication and onboarding processes (link to be created)
- [[User Authentication]] — Security considerations for account creation (link to be created)

---

## 🏷️ Tags

`#dawadzlink` `#pharmacy-platform` `#supplier-management` `#algeria-healthcare` `#docker-deployment` `#optional-uploads` `#user-registration`

---

*Last updated: June 22, 2026*
