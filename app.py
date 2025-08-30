import streamlit as st
import streamlit.components.v1 as components
import gspread
import pandas as pd
from datetime import datetime, date
import json
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
from datetime import datetime
import json
from google.oauth2.service_account import Credentials

# Page configuration
st.set_page_config(
    page_title="Attendance Tracker",
    page_icon="📋",
    layout="wide"
)

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'inspired-frame-468222-e3-ca1781f4f058.json'  # Updated filename
SHEET_NAME = 'SE_ATTENDANCE-FALL_2025'  # This is the Google Sheets document name

# Student data will be loaded from Google Sheets
STUDENTS = []

@st.cache_resource
def get_google_sheets_client():
    """Initialize and return Google Sheets client"""
    try:
        # Try to use Streamlit secrets first (for cloud deployment)
        if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            # Create credentials from Streamlit secrets
            credentials_dict = dict(st.secrets['gcp_service_account'])
            credentials = Credentials.from_service_account_info(
                credentials_dict, scopes=SCOPES
            )
            client = gspread.authorize(credentials)
            return client
        else:
            # Fall back to local JSON file (for local development)
            try:
                credentials = Credentials.from_service_account_file(
                    CREDENTIALS_FILE, scopes=SCOPES
                )
                client = gspread.authorize(credentials)
                return client
            except FileNotFoundError:
                st.error("❌ **Credentials not found!**\n\n**For local development:** Place the JSON credentials file in the same directory.\n\n**For Streamlit Cloud:** Add credentials to the secrets management.")
                return None
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {str(e)}")
        return None

def get_available_worksheets(client, sheet_name):
    """Get all available worksheets in the Google Sheets document"""
    try:
        sheet = client.open(sheet_name)
        worksheets = sheet.worksheets()
        return sheet, [(ws.title, ws) for ws in worksheets]
    except gspread.SpreadsheetNotFound:
        st.error(f"Document '{sheet_name}' not found! Please make sure the document exists and is shared with the service account.")
        return None, []
    except Exception as e:
        st.error(f"Error accessing document: {str(e)}")
        return None, []

def load_students_from_worksheet(worksheet, selected_date_str=None):
    """Load student data from a specific worksheet"""
    try:
        # Get all values from the worksheet
        all_values = worksheet.get_all_values()
        
        if not all_values:
            st.error("Worksheet is empty!")
            return [], None, None
        
        # First row contains headers (Roll No, dates...)
        headers = all_values[0]
        
        if not headers or not headers[0]:
            st.error("No headers found in worksheet!")
            return [], None, None
        
        # Show header info for debugging
        st.info(f"📋 Headers found: {headers[:5]}..." if len(headers) > 5 else f"📋 Headers found: {headers}")
        
        # The first column should contain roll numbers (might be named differently)
        roll_no_column = headers[0]  # Could be "Roll No", "chat", etc.
        
        # Use selected date or default to today
        if selected_date_str is None:
            target_date_str = datetime.now().strftime("%-d/%-m/%Y")  # Format: 29/8/2025
        else:
            target_date_str = selected_date_str
        
        target_col_idx = None
        
        # Check if target date exists in headers
        for i, header in enumerate(headers):
            if header == target_date_str:
                target_col_idx = i
                break
        
        # If target date doesn't exist, we'll need to add it
        if target_col_idx is None:
            headers.append(target_date_str)
            target_col_idx = len(headers) - 1
            # Update the worksheet with new header
            worksheet.update(range_name=f"{chr(65 + target_col_idx)}1", values=[[target_date_str]])
            st.info(f"Added date column: {target_date_str}")
        else:
            st.success(f"Found existing date column: {target_date_str}")
        
        # Extract student data (skip header row)
        students = []
        for row in all_values[1:]:
            if row and row[0]:  # Make sure roll number exists
                roll_no = row[0]
                # Get current attendance status for target date (if exists)
                current_status = 'Absent'  # Default
                if target_col_idx < len(row) and row[target_col_idx]:
                    current_status = 'Present' if row[target_col_idx].upper() == 'P' else 'Absent'
                
                students.append({
                    'roll_no': roll_no,
                    'current_status': current_status
                })
        
        return students, worksheet, target_col_idx
        
    except Exception as e:
        st.error(f"Error loading students from worksheet: {str(e)}")
        return [], None, None

def get_available_sheets(client, sheet_name):
    """Get list of available worksheets in the Google Sheet"""
    try:
        sheet = client.open(sheet_name)
        worksheets = sheet.worksheets()
        return sheet, worksheets
    except gspread.SpreadsheetNotFound:
        st.error(f"Google Sheet '{sheet_name}' not found! Please make sure the sheet exists and is shared with the service account.")
        return None, []
    except Exception as e:
        st.error(f"Error accessing Google Sheet: {str(e)}")
        return None, []

def load_students_from_sheet(client, sheet_name, worksheet_name=None, selected_date_str=None):
    """Load student data from existing Google Sheet"""
    try:
        sheet = client.open(sheet_name)
        
        # If no specific worksheet is specified, let user choose
        if worksheet_name is None:
            worksheets = sheet.worksheets()
            if len(worksheets) > 1:
                st.warning(f"Found {len(worksheets)} sheets in your Google Sheet:")
                for i, ws in enumerate(worksheets):
                    st.write(f"  {i+1}. {ws.title}")
                st.error("Please specify which sheet to use by updating the SHEET_NAME variable in the code.")
                return [], None, None
            else:
                worksheet = worksheets[0]
        else:
            try:
                worksheet = sheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                st.error(f"Worksheet '{worksheet_name}' not found in sheet '{sheet_name}'")
                worksheets = sheet.worksheets()
                st.write("Available worksheets:")
                for ws in worksheets:
                    st.write(f"  - {ws.title}")
                return [], None, None
        
        # Get all values from the sheet
        all_values = worksheet.get_all_values()
        
        if not all_values:
            st.error("Sheet is empty!")
            return [], None, None
        
        # First row contains headers (Roll No, dates...)
        headers = all_values[0]
        
        # Use selected date or default to today
        if selected_date_str is None:
            target_date_str = datetime.now().strftime("%-d/%-m/%Y")  # Format: 29/8/2025
        else:
            target_date_str = selected_date_str
        
        target_col_idx = None
        
        # Check if target date exists in headers
        for i, header in enumerate(headers):
            if header == target_date_str:
                target_col_idx = i
                break
        
        # If target date doesn't exist, we'll need to add it
        if target_col_idx is None:
            headers.append(target_date_str)
            target_col_idx = len(headers) - 1
            # Update the sheet with new header
            worksheet.update(range_name=f"{chr(65 + target_col_idx)}1", values=[[target_date_str]])
            st.info(f"Added date column: {target_date_str}")
        
        # Extract student data (skip header row)
        students = []
        for row in all_values[1:]:
            if row and row[0]:  # Make sure roll number exists
                roll_no = row[0]
                # Get current attendance status for target date (if exists)
                current_status = 'Absent'  # Default
                if target_col_idx < len(row) and row[target_col_idx]:
                    current_status = 'Present' if row[target_col_idx].upper() == 'P' else 'Absent'
                
                students.append({
                    'roll_no': roll_no,
                    'current_status': current_status
                })
        
        return students, worksheet, target_col_idx
        
    except gspread.SpreadsheetNotFound:
        st.error(f"Sheet '{sheet_name}' not found! Please make sure the sheet exists and is shared with the service account.")
        return [], None, None
    except Exception as e:
        st.error(f"Error loading students from sheet: {str(e)}")
        return [], None, None

def update_attendance_in_sheet(worksheet, students_data, today_col_idx):
    """Update today's attendance in the existing sheet format"""
    try:
        # Get all values to find the correct rows
        all_values = worksheet.get_all_values()
        
        # Create a mapping of roll numbers to row indices
        roll_to_row = {}
        for i, row in enumerate(all_values[1:], start=2):  # Start from row 2 (skip header)
            if row and row[0]:
                roll_to_row[row[0]] = i
        
        # Update each student's attendance
        updates = []
        for student_data in students_data:
            roll_no = student_data['roll_no']
            status = student_data['status']
            
            if roll_no in roll_to_row:
                row_num = roll_to_row[roll_no]
                col_letter = chr(65 + today_col_idx)  # Convert to Excel column letter
                cell_range = f"{col_letter}{row_num}"
                
                # Convert status to P/A format
                cell_value = 'P' if status == 'Present' else 'A'
                updates.append({
                    'range': cell_range,
                    'values': [[cell_value]]
                })
        
        # Batch update all cells
        if updates:
            worksheet.batch_update(updates)
            return True
        return False
        
    except Exception as e:
        st.error(f"Error updating attendance: {str(e)}")
        return False

def main():
    st.title("📋 Attendance Tracker")
    st.markdown("---")
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    # Date selection
    selected_date = st.sidebar.date_input(
        "📅 Select Date for Attendance:",
        value=datetime.now().date(),
        help="Choose the date for which you want to mark attendance"
    )
    
    # Format selected date for display and processing
    selected_date_str = selected_date.strftime("%B %d, %Y")
    selected_date_sheet_format = selected_date.strftime("%-d/%-m/%Y")  # Format for sheet headers
    
    st.subheader(f"📅 Attendance Date: {selected_date_str}")
    
    # Document name configuration
    document_name = st.sidebar.text_input(
        "Google Sheets Document Name:", 
        value=SHEET_NAME,
        help="Enter the exact name of your Google Sheets document"
    )
    
    if document_name != SHEET_NAME:
        st.sidebar.info(f"Using document: {document_name}")
    
    st.markdown("### Instructions:")
    st.markdown(f"""
    1. Select the date for attendance marking using the date picker in the sidebar
    2. Make sure your Google Sheet **"{document_name}"** is shared with the service account
    3. Select which worksheet/tab to use from your Google Sheet
    4. The app will load student data from the selected sheet
    5. Toggle the attendance status for each student
    6. Click **Submit Attendance** to save attendance for the selected date
    """)
    
    st.markdown("---")
    
    # Get Google Sheets client
    client = get_google_sheets_client()
    
    if not client:
        st.error("❌ Could not connect to Google Sheets. Please check your credentials.")
        st.stop()
    
    # Get available worksheets
    if ('worksheets_loaded' not in st.session_state or 
        st.session_state.get('current_document') != document_name):
        
        with st.spinner(f"Loading worksheets from '{document_name}'..."):
            sheet, worksheets = get_available_worksheets(client, document_name)
            if not worksheets:
                st.error(f"""
                ❌ Could not find document '{document_name}' or no worksheets found.
                
                **Please check:**
                1. Document name is correct: `{document_name}`
                2. Document is shared with: `zair-service@inspired-frame-468222-e3.iam.gserviceaccount.com`
                3. Service account has 'Editor' permissions
                """)
                st.stop()
            
            st.session_state.sheet = sheet
            st.session_state.worksheets = worksheets
            st.session_state.worksheets_loaded = True
            st.session_state.current_document = document_name
            
            st.success(f"✅ Found {len(worksheets)} worksheets in '{document_name}'")
    
    # Worksheet selection
    worksheet_names = [name for name, _ in st.session_state.worksheets]
    
    # Set default to "Section B" if it exists, otherwise first worksheet
    default_index = 0
    if "Section B" in worksheet_names:
        default_index = worksheet_names.index("Section B")
    
    st.subheader("📋 Worksheet Selection")
    selected_worksheet_name = st.selectbox(
        f"Select worksheet from '{document_name}':",
        worksheet_names,
        index=default_index,
        key="worksheet_selector"
    )
    
    # Show available worksheets info
    with st.expander("📄 Available Worksheets", expanded=False):
        for i, name in enumerate(worksheet_names, 1):
            if name == selected_worksheet_name:
                st.write(f"**{i}. {name}** ← Currently selected")
            else:
                st.write(f"{i}. {name}")
    
    # Find the selected worksheet object
    selected_worksheet = None
    for name, ws in st.session_state.worksheets:
        if name == selected_worksheet_name:
            selected_worksheet = ws
            break
    
    if not selected_worksheet:
        st.error("Selected worksheet not found!")
        st.stop()
    
    st.info(f"📊 Using worksheet: **{selected_worksheet_name}**")
    
    st.markdown("---")
    
    # Load students from selected worksheet
    if ('students_loaded' not in st.session_state or 
        st.session_state.get('current_worksheet') != selected_worksheet_name or
        st.session_state.get('selected_date') != selected_date_sheet_format):
        
        with st.spinner(f"Loading students from '{selected_worksheet_name}' for {selected_date_str}..."):
            students, worksheet, target_col_idx = load_students_from_worksheet(selected_worksheet, selected_date_sheet_format)
            
            if not students:
                st.error("❌ Could not load students from worksheet. Please check your sheet setup.")
                st.stop()
            
            st.session_state.students = students
            st.session_state.worksheet = worksheet
            st.session_state.target_col_idx = target_col_idx
            st.session_state.students_loaded = True
            st.session_state.current_worksheet = selected_worksheet_name
            st.session_state.selected_date = selected_date_sheet_format
            
            # Initialize attendance state
            st.session_state.attendance = {
                student['roll_no']: {
                    'status': student['current_status']
                }
                for student in students
            }
            
            st.success(f"✅ Loaded {len(students)} students from '{selected_worksheet_name}'!")
    
    # Use cached data
    students = st.session_state.students
    worksheet = st.session_state.worksheet
    target_col_idx = st.session_state.target_col_idx
    
    # Interface mode selection
    st.subheader("🎓 Student Attendance")
    
    # Mode selection
    interface_mode = st.radio(
        "Choose interface mode:",
        ["🚀 Fast Mode (Keyboard Navigation)", "📋 Table Mode (Click Interface)"],
        index=0,
        horizontal=True
    )
    
    if interface_mode.startswith("🚀"):
        # Fast keyboard navigation mode
        st.markdown("---")
        st.markdown("### 🚀 Fast Mode Controls")
        
        # Hotkey legend in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info("**Click:** Previous/Next")
        with col2:
            st.info("**Click:** Toggle Status")
        with col3:
            st.warning("**Click:** Present + Next")
        with col4:
            st.success("**Click:** Auto-advance Mode")
        
        # Initialize current student index
        if 'current_student_index' not in st.session_state:
            st.session_state.current_student_index = 0
        
        # Ensure index is within bounds
        if st.session_state.current_student_index >= len(students):
            st.session_state.current_student_index = 0
        if st.session_state.current_student_index < 0:
            st.session_state.current_student_index = len(students) - 1
        
        current_idx = st.session_state.current_student_index
        current_student = students[current_idx]
        
        # Navigation controls with better key handling
        st.markdown("### 🎮 Navigation Controls")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        
        with col1:
            if st.button("⬆️ Previous", key="nav_up", help="Previous student"):
                st.session_state.current_student_index = max(0, current_idx - 1)
                st.rerun()
        
        with col2:
            if st.button("⬇️ Next", key="nav_down", help="Next student"):
                st.session_state.current_student_index = min(len(students) - 1, current_idx + 1)
                st.rerun()
        
        with col3:
            current_status = st.session_state.attendance[current_student['roll_no']]['status']
            if st.button(
                f"🔄 Toggle ({current_status})", 
                key="fast_toggle",
                type="primary",
                help="Toggle Present/Absent"
            ):
                new_status = 'Present' if current_status == 'Absent' else 'Absent'
                st.session_state.attendance[current_student['roll_no']]['status'] = new_status
                st.rerun()
        
        with col4:
            if st.button("✅ Present + Next", key="next_present", help="Mark Present and go to next"):
                st.session_state.attendance[current_student['roll_no']]['status'] = 'Present'
                st.session_state.current_student_index = min(len(students) - 1, current_idx + 1)
                st.rerun()
        
        with col5:
            if st.button("❌ Absent + Next", key="next_absent", help="Mark Absent and go to next"):
                st.session_state.attendance[current_student['roll_no']]['status'] = 'Absent'
                st.session_state.current_student_index = min(len(students) - 1, current_idx + 1)
                st.rerun()
        
        # Add keyboard shortcut instructions  
        st.info("💡 **Keyboard Shortcuts**: Press Q (Previous), E (Next), W (Toggle Present/Absent)")
        
        # Add keyboard event handler
        keyboard_script = f"""
        <script>
        document.addEventListener('keydown', function(event) {{
            // Only trigger if not typing in an input field
            if (event.target.tagName !== 'INPUT' && event.target.tagName !== 'TEXTAREA') {{
                const key = event.key.toLowerCase();
                
                if (key === 'q') {{
                    // Find and click Previous button
                    const prevBtn = Array.from(document.querySelectorAll('button')).find(btn => 
                        btn.textContent.includes('Previous') || btn.textContent.includes('⬅️')
                    );
                    if (prevBtn) {{
                        prevBtn.click();
                        event.preventDefault();
                    }}
                }} else if (key === 'e') {{
                    // Find and click Next button  
                    const nextBtn = Array.from(document.querySelectorAll('button')).find(btn => 
                        btn.textContent.includes('⏭️ SKIP') || btn.textContent.includes('Next Only')
                    );
                    if (nextBtn) {{
                        nextBtn.click();
                        event.preventDefault();
                    }}
                }} else if (key === 'w') {{
                    // Toggle between Present/Absent based on current status
                    const currentStatus = '{current_student.get("status", "Absent")}';
                    
                    if (currentStatus === 'Present') {{
                        // Click Mark Absent button
                        const absentBtn = Array.from(document.querySelectorAll('button')).find(btn => 
                            btn.textContent.includes('❌ MARK ABSENT')
                        );
                        if (absentBtn) {{
                            absentBtn.click();
                            event.preventDefault();
                        }}
                    }} else {{
                        // Click Mark Present button
                        const presentBtn = Array.from(document.querySelectorAll('button')).find(btn => 
                            btn.textContent.includes('✅ MARK PRESENT')
                        );
                        if (presentBtn) {{
                            presentBtn.click(); 
                            event.preventDefault();
                        }}
                    }}
                }}
            }}
        }});
        </script>
        """
        
        components.html(keyboard_script, height=0)
        
        # Alternative: Use columns for faster clicking
        st.markdown("---")
        st.markdown("### ⚡ Super Fast Controls")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Quick navigation
            st.markdown("**Quick Jump:**")
            jump_to = st.number_input(
                "Go to student #:", 
                min_value=1, 
                max_value=len(students), 
                value=current_idx + 1,
                key="jump_to_student"
            )
            if st.button("🎯 Jump", key="jump_button"):
                st.session_state.current_student_index = jump_to - 1
                st.rerun()
        
        with col2:
            # Bulk actions
            st.markdown("**Bulk Actions:**")
            bulk_col1, bulk_col2 = st.columns(2)
            
            with bulk_col1:
                if st.button("🟢 Mark All Present", key="all_present"):
                    for student in students:
                        st.session_state.attendance[student['roll_no']]['status'] = 'Present'
                    st.rerun()
            
            with bulk_col2:
                if st.button("🔴 Mark All Absent", key="all_absent"):
                    for student in students:
                        st.session_state.attendance[student['roll_no']]['status'] = 'Absent'
                    st.rerun()
        
        with col3:
            # Speed controls
            st.markdown("**Auto-advance:**")
            auto_advance = st.checkbox("Auto-next after marking", key="auto_advance")
            
            if auto_advance:
                st.info("🚀 Auto-advance ON: Buttons will automatically move to next student")
        
        # Current student display
        st.markdown("---")
        
        # Progress indicator
        progress = (current_idx + 1) / len(students)
        st.progress(progress, text=f"Student {current_idx + 1} of {len(students)}")
        
        # Large display of current student
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### � Current Student")
            
            # Student info box
            current_status = st.session_state.attendance[current_student['roll_no']]['status']
            original_status = current_student['current_status']
            
            status_color = "🟢" if current_status == 'Present' else "🔴"
            original_color = "🟢" if original_status == 'Present' else "🔴"
            
            st.markdown(f"""
            <div style="
                border: 3px solid #1f77b4;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f0f8ff;
                margin: 10px 0;
            ">
                <h2 style="margin: 0; color: #1f77b4;">{current_student['roll_no']}</h2>
                <hr>
                <p style="font-size: 18px; margin: 10px 0;">
                    <strong>Original:</strong> {original_color} {original_status}
                </p>
                <p style="font-size: 24px; margin: 10px 0;">
                    <strong>New Status:</strong> {status_color} <span style="color: {'green' if current_status == 'Present' else 'red'};">{current_status}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Auto-advance logic for faster workflow
        if 'auto_advance' in st.session_state and st.session_state.auto_advance:
            # Automatically move to next student after marking
            pass  # This is handled in the button logic above
        
        # Enhanced large buttons for faster clicking
        st.markdown("---")
        st.markdown("### ⚡ Super Fast Actions (Large Buttons)")
        
        big_col1, big_col2, big_col3 = st.columns(3)
        
        with big_col1:
            if st.button("✅ MARK PRESENT", key="super_present", type="primary", use_container_width=True):
                st.session_state.attendance[current_student['roll_no']]['status'] = 'Present'
                if current_idx < len(students) - 1:
                    st.session_state.current_student_index = current_idx + 1
                st.rerun()
        
        with big_col2:
            if st.button("❌ MARK ABSENT", key="super_absent", use_container_width=True):
                st.session_state.attendance[current_student['roll_no']]['status'] = 'Absent'
                if current_idx < len(students) - 1:
                    st.session_state.current_student_index = current_idx + 1
                st.rerun()
        
        with big_col3:
            if st.button("⏭️ SKIP (Next)", key="super_skip", use_container_width=True):
                if current_idx < len(students) - 1:
                    st.session_state.current_student_index = current_idx + 1
                st.rerun()
        
        # Navigation shortcuts
        st.markdown("---")
        nav_shortcuts_col1, nav_shortcuts_col2, nav_shortcuts_col3, nav_shortcuts_col4 = st.columns(4)
        
        with nav_shortcuts_col1:
            if current_idx > 0 and st.button("⬅️ Previous", key="shortcut_prev", use_container_width=True):
                st.session_state.current_student_index = current_idx - 1
                st.rerun()
        
        with nav_shortcuts_col2:
            if current_idx < len(students) - 1 and st.button("➡️ Next Only", key="shortcut_next", use_container_width=True):
                st.session_state.current_student_index = current_idx + 1
                st.rerun()
        
        with nav_shortcuts_col3:
            if st.button("🎯 First Student", key="shortcut_first", use_container_width=True):
                st.session_state.current_student_index = 0
                st.rerun()
        
        with nav_shortcuts_col4:
            if st.button("🏁 Last Student", key="shortcut_last", use_container_width=True):
                st.session_state.current_student_index = len(students) - 1
                st.rerun()
        
        # Quick overview of remaining students
        with st.expander("📊 Quick Overview", expanded=False):
            remaining_students = []
            for i, student in enumerate(students):
                status = st.session_state.attendance[student['roll_no']]['status']
                marker = "👆" if i == current_idx else ("✅" if status == 'Present' else "❌")
                remaining_students.append(f"{marker} {student['roll_no']} - {status}")
            
            st.text("\n".join(remaining_students))
    
    else:
        # Original table mode
        st.markdown("---")
        st.markdown("### 📋 Table Mode")
        
        # Use columns for better layout
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            st.markdown("**Roll No**")
        with col2:
            st.markdown("**Current Status**")
        with col3:
            st.markdown("**New Status**")
        with col4:
            st.markdown("**Toggle**")
        
        st.markdown("---")
        
        # Create attendance rows (only for table mode)
        for student in students:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            
            with col1:
                st.write(student['roll_no'])
            
            with col2:
                # Show original status from sheet
                if student['current_status'] == 'Present':
                    st.success("✅ Present")
                else:
                    st.error("❌ Absent")
            
            with col3:
                # Show new status
                current_status = st.session_state.attendance[student['roll_no']]['status']
                if current_status == 'Present':
                    st.success("✅ Present")
                else:
                    st.error("❌ Absent")
            
            with col4:
                current_status = st.session_state.attendance[student['roll_no']]['status']
                if st.button(
                    "Mark Present" if current_status == 'Absent' else "Mark Absent",
                    key=f"table_toggle_{student['roll_no']}",
                    type="primary" if current_status == 'Absent' else "secondary"
                ):
                    # Toggle status
                    new_status = 'Present' if current_status == 'Absent' else 'Absent'
                    st.session_state.attendance[student['roll_no']]['status'] = new_status
                    st.rerun()
    
    st.markdown("---")
    
    # Summary
    total_students = len(students)
    present_count = sum(1 for data in st.session_state.attendance.values() if data['status'] == 'Present')
    absent_count = total_students - present_count
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", total_students)
    with col2:
        st.metric("Present", present_count, delta=None)
    with col3:
        st.metric("Absent", absent_count, delta=None)
    
    st.markdown("---")
    
    # Submit button
    if st.button(f"📤 Submit Attendance for {selected_date_str}", type="primary", use_container_width=True):
        # Prepare attendance data
        attendance_data = []
        for roll_no, data in st.session_state.attendance.items():
            attendance_data.append({
                'roll_no': roll_no,
                'status': data['status']
            })
        
        # Update attendance in sheet
        with st.spinner("Updating attendance in Google Sheet..."):
            if update_attendance_in_sheet(worksheet, attendance_data, target_col_idx):
                st.success(f"✅ Attendance for {selected_date_str} updated successfully in Google Sheet!")
                st.balloons()
                
                # Show summary
                with st.expander("📊 Submission Summary", expanded=True):
                    df = pd.DataFrame([
                        {
                            'Roll No': item['roll_no'],
                            'Status': item['status']
                        }
                        for item in attendance_data
                    ])
                    st.dataframe(df, use_container_width=True)
                    
                    # Reset for next session (optional)
                    if st.button("🔄 Reload from Sheet"):
                        # Clear session state to reload fresh data
                        for key in ['students_loaded', 'students', 'worksheet', 'target_col_idx', 'attendance', 'current_worksheet', 'selected_date', 'current_student_index']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.rerun()
            else:
                st.error("❌ Failed to update attendance. Please check your connection and try again.")
    
    # Add refresh button
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reload Students from Sheet"):
            # Clear cached data to reload
            for key in ['students_loaded', 'students', 'worksheet', 'target_col_idx', 'attendance', 'current_worksheet', 'selected_date', 'current_student_index']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("📋 Change Document/Worksheet"):
            # Clear all cached data to allow selecting different document/worksheet
            for key in ['worksheets_loaded', 'students_loaded', 'students', 'worksheet', 'target_col_idx', 'attendance', 'current_worksheet', 'current_document', 'selected_date', 'current_student_index']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("*Attendance Tracker - Powered by Streamlit & Google Sheets*")

if __name__ == "__main__":
    main()
