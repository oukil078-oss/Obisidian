---
skill: "database-migration-backward-compat-testing"
category: "software-development"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\software-development\database-migration-backward-compat-testing\SKILL.md"
vault_path: "Skills/software-development/database-migration-backward-compat-testing.md"
tags: ["software-development", "hermes-skill", "skill", "database", "migration", "testing", "backward-compatibility", "regression"]
trigger_keywords: ["test", "that", "schema", "changes", "optional", "columns", "modified", "fields", "break", "existing"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: database-migration-backward-compat-testing
description: "Test that schema changes (new optional columns, modified fields) don't break existing data or queries."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [database, migration, testing, backward-compatibility, regression]
---

# Database Migration Backward Compatibility Testing

## Overview

Use when introducing schema changes to an existing database where you must verify that:
- Existing records with `NULL` or empty values in new columns work correctly
- Queries remain flexible (don't filter out legacy data)
- Form validation accepts optional fields for all user types
- No regression occurs for existing functionality

This skill focuses on **backward compatibility verification** after schema changes, distinct from test-driven development (which writes tests before implementation).

## When to Use

Create and run backward compatibility tests when:

- ✅ Adding new optional columns with default values (`NULL`, `''`, or computed defaults)
- ✅ Modifying existing nullable fields to accept more input patterns
- ✅ Making required fields optional for specific user types
- ✅ Implementing feature flags or document optionality logic
- ✅ Performing database migrations that introduce new attributes

### Don't Use For

- ❌ First-time schema creation (no legacy data concerns)
- ❌ Standard unit/integration tests (use `test-driven-development`)
- ❌ Performance testing or load testing
- ❌ Security scanning tasks

## Trigger Conditions

Run this skill when:
1. Schema migration is complete (column added, type changed, constraint modified)
2. New optional field needs to accept `NULL`, empty string, and actual values
3. Existing users must continue working with their legacy data intact
4. Form validation must not require the new field for all user types

## Required Environment Variables

| Variable | Description | Typical Value |
|----------|-------------|---------------|
| `DATABASE_PATH` | Absolute path to SQLite/PostgreSQL database | `/vagrant/database.db`, `~/data.db` |
| `FLASK_APP` | Flask application entry point (if applicable) | `src:app` |

Set these before running migration tests for consistency across environments.

## Standard Workflow

### 1. Schema Verification

First, verify the schema change was applied correctly:

```python
import sqlite3

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Check column exists and is nullable
cursor.execute("""
    SELECT 
        name, 
        sql 
    FROM pragma_table_info('users') 
    WHERE name = 'registry_number'
""")
result = cursor.fetchone()

if result:
    print(f"✓ Column found: {result[0]}")
    print(f"  Definition: {result[1]}")
    
    # Verify nullable
    if 'nullable' in result[1].lower() or 'NOT NULL' not in result[1]:
        print("  → Column is nullable (accepts NULL)")
else:
    print("✗ Column not found - migration may have failed")

conn.close()
```

### 2. Data Inspection Queries

Build queries to inspect existing legacy data:

```python
# Count records with empty/NULL values in the new field
cursor.execute("""
    SELECT COUNT(*) as count 
    FROM users 
    WHERE registry_number IS NULL OR registry_number = ''
""")
print(f"Users with empty registry_number: {cursor.fetchone()[0]}")

# List sample legacy users (top 10)
cursor.execute("""
    SELECT id, email, name, last_name, first_name 
    FROM users 
    WHERE is_superuser = 0 
    ORDER BY id ASC 
    LIMIT 10
""")
legacy_users = cursor.fetchall()
print(f"Legacy user count: {len(legacy_users)}")

# Check for any corrupted/invalid data patterns
cursor.execute("""
    SELECT COUNT(*) as invalid_count 
    FROM users 
    WHERE registry_number LIKE '%%%' 
      AND (registry_number IS NULL OR length(registry_number) < 3)
""")
print(f"Potentially invalid entries: {cursor.fetchone()[0]}")
```

### 3. Flexible Query Pattern Verification

Ensure queries don't filter on the optional field strictly:

```python
# ❌ DON'T: Filter that breaks for empty fields
bad_query = """
    SELECT * FROM users WHERE registry_number = 'X'
"""

# ✅ DO: Use flexible patterns
good_queries = [
    # Primary key query (works regardless of optional field)
    "SELECT * FROM users WHERE id=:user_id",
    
    # Coalesce pattern for equality checks
    "SELECT * FROM users WHERE COALESCE(registry_number, '') = :val",
    
    # Range query with coalesce
    "SELECT * FROM users WHERE registry_number IS NOT NULL AND length(registry_number) > 3",
]

# Test each query pattern
for query_name, sql in [
    ("Primary Key", "id=:user_id"),
    ("Coalesce Empty", "COALESCE(registry_number, '') = :val"),
]:
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE {sql}", 
                   {"val": "", "user_id": 1})
    print(f"✓ Query '{query_name}' works: {cursor.fetchone()[0]} rows")
```

### 4. User Type Filtering Tests

Verify that optional field logic doesn't break specific user types:

```python
# Test 1: Regular users (is_superuser=0) with empty fields
cursor.execute("""
    SELECT id, email, registry_number 
    FROM users 
    WHERE is_superuser = 0 
    AND (registry_number IS NULL OR registry_number = '') 
    LIMIT 5
""")
regular_users = cursor.fetchall()
print(f"Regular users with empty field: {len(regular_users)}")

# Test 2: Admin/superuser accounts
cursor.execute("""
    SELECT id, email, registry_number 
    FROM users 
    WHERE is_superuser = 1 
    LIMIT 3
""")
superusers = cursor.fetchall()
print(f"Superuser count: {len(superusers)}")

# Test 3: Users with actual registry numbers
cursor.execute("""
    SELECT COUNT(*) as total 
    FROM users 
    WHERE registry_number IS NOT NULL 
      AND registry_number != ''
""")
print(f"Users with non-empty registry_number: {cursor.fetchone()[0]}")
```

### 5. Form Validation Tests (Flask)

If using Flask/Werkzeug forms, test validation logic:

```python
from flask import Flask
from src.forms.users import UserForm

def test_form_validation():
    app = Flask(__name__)
    
    with app.app_context():
        # Test 1: Empty data submission (should work for optional fields)
        data = {
            'email': 'new@example.com',
            'password': 'SecurePass123!'
            # No registry_number or documents provided
        }
        
        form = UserForm()
        with app.test_request_context('/', method='POST', data=data):
            if form.validate():
                print("✓ Form accepts empty registry_number submission")
            else:
                errors = {k: v for k, v in form.errors.items()}
                if 'registry_number' in errors:
                    print(f"✗ Registry number incorrectly required: {errors['registry_number']}")

# Run validation tests
test_form_validation()
```

### 6. Model Integration Tests

Verify model queries work with legacy data:

```python
from src.models.User import User
from src.database.db_connection import get_db

def test_model_queries():
    db = get_db()
    
    # Test 1: Query user by primary key (always works)
    user_id = 1
    query = "SELECT * FROM users WHERE id = :id"
    result = db.execute(text(query), {"id": user_id}).fetchone()
    if result:
        print(f"✓ Primary key query works for ID {user_id}")
        print(f"  Email: {result[1]}, Registry: {result[5]}")
    
    # Test 2: Aggregate queries (don't filter on optional field)
    query = """
        SELECT 
            COUNT(*) as total_users,
            SUM(CASE WHEN registry_number IS NOT NULL THEN 1 ELSE 0 END) as with_registry,
            AVG(id) as avg_id
        FROM users
    """
    result = db.execute(text(query)).fetchone()
    print(f"✓ Aggregate query works: {result[0]} total users")

test_model_queries()
```

## Reference Files Structure

### `references/schema-migration-checklist.md`
Detailed checklist for validating schema migrations before/after deployment.

### `references/cross-platform-db-path-handling.md`
Guidance for handling different database paths across Linux (`/vagrant/database.db`) and Windows environments.

### `templates/test_backward_compat.py.template`
Starter template for creating backward compatibility test scripts.

## Common Pitfalls

### 1. Assuming SQLite Auto-Creates Columns ✅

SQLite will auto-create columns if they're referenced, but with caveats:

```python
# ✅ Safe: Column creation happens automatically on first write
user = User(id=99, email="test@example.com")
db.add(user)
db.commit()  # Column created if it didn't exist

# ⚠️ Caution: This won't preserve default values or constraints
```

### 2. Forgetting Primary Key Queries ✅

Primary key queries always work regardless of optional fields:

```python
# ✅ Always use primary keys for user lookups
user = db.query("SELECT * FROM users WHERE id=:id", {"id": user_id})

# ❌ Don't query by optional field value
user = db.query("SELECT * FROM users WHERE email=:email", {"email": "test@example.com"})  # May miss empty-field users
```

### 3. Query Filtering on Optional Fields ✅

Queries must handle `NULL`/empty gracefully:

```python
# ❌ Problematic (filters out empty fields)
query = "SELECT * FROM users WHERE registry_number = 'XYZ'"

# ✅ Safe alternatives
queries = [
    "SELECT * FROM users WHERE id=:id",  # Primary key query
    "SELECT * FROM users WHERE COALESCE(registry_number, '') != ''",  # Exclude empty explicitly
    "SELECT * FROM users",  # Get all, filter in application code if needed
]
```

### 4. Form Validation Making Fields Required ✅

Form validation should allow optional fields for legacy compatibility:

```python
class UserForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make optional for backward compatibility
        self.fields['registry_number'].required = False
    
    def validate(self):
        # Only require if documents are selected
        if self.data.get('documents') and not self.data.get('registry_number'):
            # Either accept empty or set to default
            self.process_data()  # Let database handle defaults
        
        return True
```

### 5. Environment Path Mismatches ✅

Different environments require explicit path handling:

```python
import os

# ❌ Don't assume relative paths work everywhere
database_path = "database.db"  # May fail on production server

# ✅ Use hardcoded absolute path or environment variable
database_paths = {
    "development": os.path.expanduser("~/data/database.db"),
    "vagrant": "/vagrant/database.db",      # Linux VM path
    "production": "/app/data/prod.db"       # Production path
}

DB_PATH = database_paths.get(os.getenv("ENV", "development"), 
                            os.path.expanduser("~/data/database.db"))
```

## Verification Checklist

Before deploying schema changes:

- [ ] Schema migration script executed successfully
- [ ] Column exists with correct type (e.g., `TEXT`, `VARCHAR(100)`)
- [ ] Column is nullable (`nullable=True` or no `NOT NULL` constraint)
- [ ] Default value set if column wasn't explicitly nullable (use application defaults)
- [ ] Legacy data inspection shows expected count of empty/NULL records
- [ ] Primary key queries work for existing users
- [ ] Flexible query patterns tested with sample legacy data
- [ ] Form validation accepts empty values for optional fields
- [ ] No regression in login/profile/dashboard functionality
- [ ] Documentation updated to reflect new optional field usage

## One-Shot Recipes

### Quick Compatibility Check (5 minutes)

```bash
cd "C:/Users/pc/Documents/Vs-Code/Mind-Galaxy"

# Run comprehensive backward compatibility test
python tests/test_backward_compatibility.py
```

**What it verifies:**
1. Existing users with empty `registry_number` can log in
2. Profile view displays correctly for legacy users
3. User queries return data without filtering on optional fields
4. New registration accepts optional document selection

### Manual SQL Check (2 minutes)

```bash
sqlite3 database.db <<EOF
SELECT 
    '=== Existing Users ===' as info;
SELECT id, email, name, last_name, first_name 
FROM users WHERE is_superuser=0 LIMIT 10;

SELECT '=== Empty Registry Number Count ===' as info;
SELECT COUNT(*) as count 
FROM users WHERE registry_number IS NULL OR registry_number = '';

SELECT '=== Flexible Query Test ===' as info;
SELECT id, email FROM users WHERE id IN (SELECT id FROM users WHERE is_superuser=0 LIMIT 5);
EOF
```

### Python Direct Check (1 minute)

```python
from src.database.db_connection import get_db
from sqlalchemy import text

db = get_db()

# Quick compatibility check
checks = [
    ("Existing user query", 
     "SELECT id, email FROM users WHERE is_superuser = 0 LIMIT 5"),
    ("Empty field count", 
     "SELECT COUNT(*) FROM users WHERE registry_number IS NULL OR registry_number = ''"),
]

for name, sql in checks:
    result = db.execute(text(sql)).fetchall()
    print(f"✓ {name}: {len(result) if result else 0} rows")
```

## Example Reference Files

### `references/schema-migration-checklist.md` (content summary)

- Pre-migration data backup procedure
- Post-migration schema verification steps
- Legacy data inspection queries
- Rollback plan for failed migrations
- Environment-specific path configuration

### `references/cross-platform-db-path-handling.md` (content summary)

- Linux: `/vagrant/database.db` (common in vagrant VMs)
- Windows: `C:/Users/<user>/data/database.db` or relative paths
- Docker: `/app/data/database.db` (inside container)
- Environment variable pattern: `DATABASE_PATH` vs hardcoded paths
- Path consistency checks across development/staging/production

### `templates/test_backward_compat.py.template` (content summary)

- Template for creating new backward compatibility test scripts
- Standard test functions (login, profile, query, registration)
- Common SQL verification queries
- Test reporting format and expected success messages

---

*Skill authored by Hermes Agent for database migration workflows*
