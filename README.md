# Attendance Tracker App

A Streamlit-based attendance tracking application that loads student data from existing Google Sheets and updates attendance for today's date.

## Features

- **Multiple Worksheet Support**: Automatically detects all worksheets/tabs in your Google Sheet
- **Worksheet Selection**: Choose which worksheet to use (defaults to "Section B" if available)
- **Load Students from Google Sheets**: Automatically reads student roll numbers from your existing sheet
- **Date-based Columns**: Works with existing format where each date is a column
- **Smart Date Handling**: Automatically adds today's date column if it doesn't exist
- **Interactive Toggle Interface**: Easy Present/Absent toggles for each student
- **Real-time Updates**: Updates the existing Google Sheet with today's attendance
- **Summary Dashboard**: Shows total students, present count, and absent count
- **Sheet Format Support**: Works with format like `Roll No | 22/8/2025 | 27/8/2025 | 29/8/2025`

## Setup Instructions

### 1. Google Sheets Setup

**Your Google Sheets document should be named: `SE_ATTENDANCE-FALL_2025`**

**Document Structure:**
```
Document: SE_ATTENDANCE-FALL_2025
├── Sheet 1 (e.g., "Section A")
└── Sheet 2 (e.g., "Section B")
```

**Each worksheet should have the following format:**

```
Roll No     | 22/8/2025 | 27/8/2025 | 29/8/2025
BSCS 21104  | A         | P         | 
BSCS 22004  | P         | P         | 
BSCS 22006  | A         | P         | 
BSCS 22008  | P         | P         | 
```

**Setup Steps:**
1. Make sure your Google Sheet document is named **"SE_ATTENDANCE-FALL_2025"**
2. Each worksheet/tab should contain student data in the format above
3. First column should contain roll numbers (like "BSCS 21104", "BSCS 22004", etc.)
4. Subsequent columns should be dates in format `d/m/yyyy` (like "22/8/2025")
5. Use "P" for Present and "A" for Absent in data cells
6. Share the document with your service account email: `zair-service@inspired-frame-468222-e3.iam.gserviceaccount.com`
7. Grant **"Editor"** permissions to the service account

**Note:** The app will automatically add today's date as a new column if it doesn't exist.

### 2. Installation

1. Make sure you have Python 3.7+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Running the App

1. Navigate to the project directory:
   ```bash
   cd /home/zair/Documents/attendence
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and go to `http://localhost:8501`

## How to Use

1. **Select Worksheet**: The app will show all available worksheets/tabs and let you choose (defaults to "Section B")
2. **Load Students**: The app automatically loads all student roll numbers from the selected worksheet
3. **View Current Status**: See each student's current attendance status from the sheet
4. **Mark Today's Attendance**: Use toggle buttons to mark students as Present/Absent for today
5. **Review Summary**: Check the summary section showing total counts
6. **Submit**: Click "Submit Today's Attendance" to update the Google Sheet
7. **Change Worksheet**: Use "Change Worksheet" button to select a different tab
8. **Reload**: Use "Reload Students from Sheet" to refresh data from the current worksheet

## Customization

### Sheet Name

If your attendance sheet has a different name, modify the `SHEET_NAME` constant in `app.py`:

```python
SHEET_NAME = 'Your_Sheet_Name'
```

### Date Format

The app expects dates in format `d/m/yyyy` (e.g., "29/8/2025"). If you use a different format, modify the date formatting in the `load_students_from_sheet` function.

## Google Sheets Output Format

The app works with your existing format and adds today's date as a new column:

**Before:**
| Roll No     | 22/8/2025 | 27/8/2025 |
|-------------|-----------|-----------|
| BSCS 21104  | A         | P         |
| BSCS 22004  | P         | P         |

**After (today is 29/8/2025):**
| Roll No     | 22/8/2025 | 27/8/2025 | 29/8/2025 |
|-------------|-----------|-----------|-----------|
| BSCS 21104  | A         | P         | P         |
| BSCS 22004  | P         | P         | A         |

## Troubleshooting

### Common Issues:

1. **"Error connecting to Google Sheets"**
   - Check that `credentials.json` exists in the project directory
   - Verify the service account has proper permissions

2. **"SpreadsheetNotFound"**
   - The app will automatically create a new sheet named "Attendance"
   - Make sure the service account has drive creation permissions

3. **Permission Denied**
   - Share your Google Sheet with the service account email
   - Grant "Editor" permissions

## File Structure

```
attendence/
├── app.py                          # Main Streamlit application
├── credentials.json                # Google service account credentials
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## Security Notes

- Keep `credentials.json` secure and never commit it to public repositories
- The current credentials file contains a valid service account key
- Consider rotating keys regularly for security

## Support

If you encounter any issues:
1. Check that all dependencies are installed correctly
2. Verify Google Sheets API is enabled for your project
3. Ensure proper permissions are set for the service account
4. Check the Streamlit logs for detailed error messages
# Attendence-system
