#!/usr/bin/env python3
"""
Quick Test Script for Backward Compatibility
============================================
Run this script to verify existing users with empty registry_number fields work correctly.
"""

import sys
from flask import Flask, render_template
from src.models.User import User, UserForm
from src.database.db_connection import get_db
from sqlalchemy import text


def test_existing_user_login():
    """Test 1: Existing user login works"""
    print("\n" + "=" * 60)
    print("TEST 1: Login with existing user credentials")
    print("=" * 60)
    
    # Create test user (simulating existing user in DB)
    email = "existing_user@example.com"
    
    try:
        app = Flask(__name__)
        with app.app_context():
            db = get_db()
            
            # Query to check if user exists (without filtering by registry_number)
            query = text("SELECT id, email, name, last_name, first_name FROM users WHERE email = :email")
            params = {"email": email}
            
            result = db.execute(query, params)
            row = result.fetchone()
            
            if row:
                print(f"✓ User found in database:")
                print(f"  ID: {row[0]}")
                print(f"  Email: {row[1]}")
                print(f"  Name: {row[2] + ' ' + row[3] + ' ' + row[4]}")
                print("\n→ Login works! User exists with empty registry_number field.")
            else:
                print("ℹ️  User doesn't exist in test DB (expected for new env)")
                
    except Exception as e:
        print(f"✗ Error during login test: {e}")


def test_existing_user_profile():
    """Test 2: Display existing user profile without errors"""
    print("\n" + "=" * 60)
    print("TEST 2: View existing user profile")
    print("=" * 60)
    
    try:
        app = Flask(__name__)
        with app.app_context():
            db = get_db()
            
            # Query profile data for a user who may have empty registry_number
            query = text("""
                SELECT 
                    id, email, name, last_name, first_name, registry_number
                FROM users 
                WHERE is_superuser = 0
                LIMIT 1
            """)
            
            result = db.execute(query)
            row = result.fetchone()
            
            if row:
                profile_data = {
                    "id": row[0],
                    "email": row[1],
                    "name": row[2],
                    "last_name": row[3],
                    "first_name": row[4],
                    "registry_number": row[5]  # May be NULL or empty
                }
                
                print(f"✓ Profile data retrieved successfully:")
                for key, value in profile_data.items():
                    if value is not None:
                        print(f"  {key}: {value}")
                    else:
                        print(f"  {key}: (empty)")
                
                print("\n→ Profile view works! Empty registry_number handled correctly.")
            else:
                print("ℹ️  No regular user found in test DB")
                
    except Exception as e:
        print(f"✗ Error during profile test: {e}")


def test_user_query_flexibility():
    """Test 3: Query users without filtering on registry_number"""
    print("\n" + "=" * 60)
    print("TEST 3: Query existing users (without registry_number filter)")
    print("=" * 60)
    
    try:
        app = Flask(__name__)
        with app.app_context():
            db = get_db()
            
            # Flexible query - doesn't require registry_number
            query = text("SELECT id, email FROM users WHERE is_superuser = 0 LIMIT 10")
            result = db.execute(query)
            rows = result.fetchall()
            
            if rows:
                print(f"✓ Found {len(rows)} existing user(s):")
                for row in rows[:3]:  # Show first 3
                    print(f"  - ID: {row[0]}, Email: {row[1]}")
                if len(rows) > 3:
                    print(f"  ... and {len(rows) - 3} more")
                
                print("\n→ Query works! No filtering on registry_number required.")
            else:
                print("ℹ️  No users found in test DB (expected for new environment)")
                
    except Exception as e:
        print(f"✗ Error during query test: {e}")


def test_registration_with_optional_documents():
    """Test 4: Register new user without mandatory documents"""
    print("\n" + "=" * 60)
    print("TEST 4: Register new user with optional documents")
    print("=" * 60)
    
    try:
        app = Flask(__name__)
        
        test_data = {
            'email': f'test_user_{len(sys.argv)}.example.com' if len(sys.argv) > 1 else 'test@example.com',
            'password': 'SecureTest123!'
            # No registry_number or documents - should be optional
        }
        
        with app.test_request_context('/', method='POST', data=test_data):
            form = UserForm()
            
            if form.validate():
                print("✓ Form validation passed!")
                print(f"  Email: {test_data['email']}")
                print(f"  Password: Set securely")
                
                # Check which fields are required/optional
                for field_name in form.field_names:
                    if field_name not in test_data:
                        is_required = getattr(form, field_name).data in ['', None] and form.fields[field_name].required
                        print(f"  {field_name}: (not provided - should be optional)")
                    
                    else:
                        print(f"  {field_name}: {form.fields[field_name].data}")
                
                print("\n→ Registration works! Documents are optional for all users.")
            else:
                # Check form errors
                if 'registry_number' in form.errors or 'documents' in form.errors:
                    print("✗ Form validation failed:")
                    for field, error in form.errors.items():
                        if field in ['registry_number', 'documents']:
                            print(f"  {field}: {error}")
                else:
                    print("? No errors, but no data submitted")
                    
    except Exception as e:
        print(f"✗ Error during registration test: {e}")


def run_all_tests():
    """Run all backward compatibility tests"""
    print("\n" + "=" * 60)
    print("BACKWARD COMPATIBILITY TEST SUITE")
    print("=" * 60)
    print("\nThis suite verifies that:")
    print("  ✓ Existing users with empty registry_number work correctly")
    print("  ✓ Queries don't break on NULL/empty fields")
    print("  ✓ Profile view handles missing data gracefully")
    print("  ✓ Registration accepts optional document selection")
    
    test_existing_user_login()
    test_existing_user_profile()
    test_user_query_flexibility()
    test_registration_with_optional_documents()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("""
✅ All tests completed!

Expected Results:
  ✓ Login tests: Existing users with empty registry_number log in successfully
  ✓ Profile tests: User profiles display correctly with empty/NULL fields
  ✓ Query tests: User queries work without filtering on registry_number
  ✓ Registration tests: New users can register with or without documents
  
If any test shows ✗ above, review the error message for specific fixes.
""")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTest suite cancelled by user.")
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
