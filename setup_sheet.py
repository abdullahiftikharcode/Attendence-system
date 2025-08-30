#!/usr/bin/env python3
"""
Google Sheet Setup Helper
This script helps you create a sample attendance sheet with the correct format
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'

# Sample data matching your format
SAMPLE_STUDENTS = [
    "BSCS 21104",
    "BSCS 22004", 
    "BSCS 22006",
    "BSCS 22008",
    "BSCS 22010",
    "BSCS 22012",
    "BSCS 22016",
    "BSCS 22018",
    "BSCS 22022",
    "BSCS 22026",
    "BSCS 22028",
    "BSCS 22030"
]

def create_sample_sheet():
    """Create a sample attendance sheet with the correct format"""
    try:
        print("🔄 Connecting to Google Sheets...")
        
        # Load credentials
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        
        sheet_name = "Attendance"
        
        # Try to open existing sheet or create new one
        try:
            sheet = client.open(sheet_name)
            print(f"📄 Found existing sheet: {sheet_name}")
            worksheet = sheet.sheet1
        except gspread.SpreadsheetNotFound:
            print(f"📝 Creating new sheet: {sheet_name}")
            sheet = client.create(sheet_name)
            worksheet = sheet.sheet1
        
        # Clear existing content
        worksheet.clear()
        
        # Create sample dates (last few days)
        today = datetime.now()
        dates = []
        for i in range(5, 0, -1):  # Last 5 days
            date = today - timedelta(days=i)
            dates.append(date.strftime("%d/%m/%Y"))
        
        # Create headers
        headers = ["Roll No"] + dates
        worksheet.append_row(headers)
        
        # Add student data with sample attendance
        import random
        for student in SAMPLE_STUDENTS:
            row = [student]
            # Add random attendance for previous dates
            for _ in dates:
                row.append(random.choice(['P', 'A']))
            worksheet.append_row(row)
        
        print(f"✅ Sample sheet created successfully!")
        print(f"🔗 Sheet URL: https://docs.google.com/spreadsheets/d/{sheet.id}")
        print(f"📧 Make sure to share with: zair-service@inspired-frame-468222-e3.iam.gserviceaccount.com")
        print(f"🔑 Grant 'Editor' permissions")
        
        # Show the data structure
        print("\n📊 Sample data structure:")
        print("Headers:", headers)
        print("Sample student rows:")
        for i, student in enumerate(SAMPLE_STUDENTS[:3]):
            sample_row = [student] + [random.choice(['P', 'A']) for _ in dates]
            print(f"  {sample_row}")
        print("  ... (and more students)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def show_format_info():
    """Show the expected format information"""
    print("\n📋 Expected Google Sheet Format:")
    print("=" * 50)
    print("Column A: Roll No (e.g., 'BSCS 21104', 'BSCS 22004')")
    print("Column B+: Dates in format d/m/yyyy (e.g., '22/8/2025')")
    print("Data cells: 'P' for Present, 'A' for Absent")
    print("\nExample:")
    print("| Roll No     | 22/8/2025 | 27/8/2025 | 29/8/2025 |")
    print("|-------------|-----------|-----------|-----------|")
    print("| BSCS 21104  | A         | P         |           |")
    print("| BSCS 22004  | P         | P         |           |")
    print("| BSCS 22006  | A         | P         |           |")
    print("\nNote: Today's column will be added automatically by the app!")

if __name__ == "__main__":
    print("🎓 Google Sheet Setup Helper")
    print("=" * 40)
    
    show_format_info()
    
    print("\n" + "=" * 50)
    choice = input("\nDo you want to create a sample sheet? (y/n): ").lower().strip()
    
    if choice == 'y':
        if create_sample_sheet():
            print("\n🎉 Setup complete! You can now run: streamlit run app.py")
        else:
            print("\n❌ Setup failed. Please check your credentials and try again.")
    else:
        print("\n💡 Manual setup: Create your sheet with the format shown above.")
        print("📧 Don't forget to share with: zair-service@inspired-frame-468222-e3.iam.gserviceaccount.com")
