#!/usr/bin/env python3
"""
Test connection to SE_ATTENDANCE-FALL_2025 document
This script will verify the connection and show available worksheets
"""

import gspread
from google.oauth2.service_account import Credentials

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
DOCUMENT_NAME = 'SE_ATTENDANCE-FALL_2025'

def test_document_access():
    """Test access to the SE_ATTENDANCE-FALL_2025 document"""
    try:
        print(f"🔄 Testing connection to '{DOCUMENT_NAME}'...")
        
        # Load credentials
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        
        # Try to open the document
        sheet = client.open(DOCUMENT_NAME)
        print(f"✅ Successfully connected to document: {DOCUMENT_NAME}")
        
        # Get all worksheets
        worksheets = sheet.worksheets()
        print(f"📋 Found {len(worksheets)} worksheet(s):")
        
        for i, ws in enumerate(worksheets, 1):
            print(f"  {i}. {ws.title} ({ws.row_count} rows, {ws.col_count} cols)")
            
            # Show first few rows of each worksheet
            try:
                values = ws.get_all_values()
                if values:
                    print(f"     Headers: {values[0][:5]}...")  # Show first 5 headers
                    if len(values) > 1:
                        print(f"     Sample data: {values[1][:3]}...")  # Show first 3 columns of first data row
                    print(f"     Total students: {len(values) - 1}")
                else:
                    print("     (Empty worksheet)")
                print()
            except Exception as e:
                print(f"     Error reading data: {str(e)}")
                print()
        
        print("🎉 Document access test successful!")
        print(f"🔗 Document URL: https://docs.google.com/spreadsheets/d/{sheet.id}")
        
        return True
        
    except gspread.SpreadsheetNotFound:
        print(f"❌ Document '{DOCUMENT_NAME}' not found!")
        print("\n🔧 Please check:")
        print(f"1. Document name is exactly: {DOCUMENT_NAME}")
        print("2. Document is shared with: zair-service@inspired-frame-468222-e3.iam.gserviceaccount.com")
        print("3. Service account has 'Editor' permissions")
        return False
        
    except Exception as e:
        print(f"❌ Error accessing document: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎓 SE_ATTENDANCE-FALL_2025 Connection Test")
    print("=" * 50)
    
    success = test_document_access()
    
    if success:
        print("\n✨ You can now run the attendance app:")
        print("   streamlit run app.py")
    else:
        print("\n❌ Please fix the issues above before running the app.")
