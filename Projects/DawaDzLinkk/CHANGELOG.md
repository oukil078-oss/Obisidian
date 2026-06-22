# 📝 DawaDzLink - Changelog

> **Release Notes** — Track all changes and updates to the project

---

## [Unreleased] — June 22, 2026

### Optional Document Uploads (Latest Update)

Made all document uploads optional for both supplier and pharmacy registration – users can now create accounts without uploading any documents.

#### Summary of Change
- **Feature:** All document uploads are now completely optional during registration
- **Impact:** Users can sign up immediately with basic info only (name, email, phone, address, password)
- **Files Modified:** `src/components/RegistrationFlow.tsx`

#### Code Changes

**Before:** Required documents were mandatory for specific user types
```typescript
// Suppliers required "Registre de commerce"
const requiredDocs: string[] = [
  'Registre de commerce', // MANDATORY
];

// Pharmacies required "Agrément de pharmacie" + "Registre de Commerce"
const requiredDocs: string[] = [
  'Agrément de pharmacie', // MANDATORY
  'Registre de Commerce',   // MANDATORY
];
```

**After:** All documents are now optional
```typescript
// NO REQUIRED DOCUMENTS — all uploads are optional
const requiredDocs: string[] = []; // Empty array means no required docs

const optionalDocs: string[] = [
  // SUPPLIERS:
  'Registre de commerce',
  'Agrément',
  'Certificat fiscal',
  
  // PHARMACIES:
  'Agrément de pharmacie',
  'Registre de Commerce',
  "Inscription à l'ordre des pharmaciens",
];
```

**Submission Check Updated:**
- **Before:** `if (!uploadedDocs.length) return;` — Blocks upload without any docs
- **After:** Always passes since there are no required docs

#### Documents Affected

**Suppliers:** All of the following became optional:
- Registre de commerce (Trade Register)
- Agrément (Commercial License)
- Certificat fiscal (Tax Certificate)

**Pharmacies:** All of the following became optional:
- Agrément de pharmacie (Pharmacy License)
- Registre de Commerce (Trade Register)
- Inscription à l'ordre des pharmaciens (Pharmacy Order Registration)

#### Testing Instructions

After rebuilding containers:
```bash
docker-compose build backend --no-cache
docker-compose up -d backend
```

1. Navigate to registration page
2. Fill in basic fields only (name, email, phone, address, password)
3. **Skip all document upload fields**
4. Submit form
5. ✅ Confirm registration succeeds without any file uploads

---

## Previous Releases

*See individual documentation files for historical changes:*
- `DOCUMENTS_OPTIONAL_CHANGES.md` — Initial optional documents implementation
- `FINAL_OPTIONAL_DOCS_SUMMARY.md` — Complete backend fix summary
- `SUCCESS_SUMMARY.md` — Final validation and deployment notes
