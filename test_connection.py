#!/usr/bin/env python3
"""
Test script to verify Google Sheets connection
Run this before using the main app to ensure everything is set up correctly
"""

import gspread
from google.oauth2.service_account import Credentials
import sys

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'

def test_connection():
    """Test Google Sheets connection"""
    try:
        print("🔄 Testing Google Sheets connection...")
        
        # Load credentials
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        
        print("✅ Successfully connected to Google Sheets!")
        print(f"📧 Service Account Email: {credentials.service_account_email}")
        
        # Try to create a test sheet
        test_sheet_name = "Attendance_Test"
        try:
            # Check if test sheet exists
            sheet = client.open(test_sheet_name)
            print(f"📄 Found existing test sheet: {test_sheet_name}")
        except gspread.SpreadsheetNotFound:
            # Create test sheet
            print(f"📝 Creating test sheet: {test_sheet_name}")
            sheet = client.create(test_sheet_name)
            worksheet = sheet.sheet1
            worksheet.append_row(['Date', 'Roll No', 'Name', 'Status'])
            print(f"✅ Test sheet created successfully!")
            print(f"🔗 Sheet URL: https://docs.google.com/spreadsheets/d/{sheet.id}")
        
        print("\n🎉 Google Sheets connection test passed!")
        print("📋 You can now run the attendance app with: streamlit run app.py")
        return True
        
    except FileNotFoundError:
        print("❌ Error: credentials.json file not found!")
        print("💡 Make sure the credentials file is in the same directory as this script")
        return False
        
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check that your service account has Google Sheets API enabled")
        print("2. Verify that the credentials.json file is valid")
        print("3. Ensure the service account has proper permissions")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
