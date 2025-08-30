#!/usr/bin/env python3
"""
Test script to verify Google Sheets connection using Streamlit secrets
This will help debug the JWT signature issue
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Test the connection using Streamlit secrets
def test_streamlit_connection():
    try:
        st.write("🔄 Testing Google Sheets connection with Streamlit secrets...")
        
        # Check if secrets are available
        if 'gcp_service_account' not in st.secrets:
            st.error("❌ No gcp_service_account found in Streamlit secrets!")
            st.write("Available secrets keys:", list(st.secrets.keys()))
            return False
        
        # Create credentials from Streamlit secrets
        credentials_dict = dict(st.secrets['gcp_service_account'])
        st.write("✅ Secrets loaded successfully")
        st.write("Keys found:", list(credentials_dict.keys()))
        
        # Create credentials object
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        st.write("✅ Credentials created successfully")
        st.write(f"Service Account Email: {credentials.service_account_email}")
        
        # Test the connection
        client = gspread.authorize(credentials)
        st.write("✅ Successfully connected to Google Sheets!")
        
        # Try to list available spreadsheets
        try:
            spreadsheets = client.openall()
            st.write(f"✅ Found {len(spreadsheets)} accessible spreadsheets")
            
            # Look for your specific sheet
            target_sheet = "SE_ATTENDANCE-FALL_2025"
            try:
                sheet = client.open(target_sheet)
                st.success(f"✅ Successfully accessed '{target_sheet}'!")
                st.write(f"Sheet ID: {sheet.id}")
                st.write(f"URL: https://docs.google.com/spreadsheets/d/{sheet.id}")
                
                # List worksheets
                worksheets = sheet.worksheets()
                st.write(f"Worksheets found: {[ws.title for ws in worksheets]}")
                
            except gspread.SpreadsheetNotFound:
                st.warning(f"⚠️ Sheet '{target_sheet}' not found")
                st.write("Available sheets:")
                for i, s in enumerate(spreadsheets[:5]):  # Show first 5
                    st.write(f"  {i+1}. {s.title}")
                if len(spreadsheets) > 5:
                    st.write(f"  ... and {len(spreadsheets) - 5} more")
                    
        except Exception as e:
            st.error(f"❌ Error listing spreadsheets: {str(e)}")
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.write("Full error details:", e)
        return False

# Main app
st.title("🔧 Google Sheets Connection Test")
st.write("This will test your Streamlit secrets configuration")

if st.button("🧪 Test Connection"):
    test_streamlit_connection()

st.markdown("---")
st.write("**Instructions:**")
st.write("1. Make sure you've added your secrets to Streamlit Cloud")
st.write("2. Click 'Test Connection' to verify everything works")
st.write("3. If successful, your main app should work too")
