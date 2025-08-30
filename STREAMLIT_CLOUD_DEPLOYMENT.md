# 🚀 Streamlit Cloud Deployment Guide

## ✅ Steps to Deploy Your Attendance App

### 1. **Upload to GitHub** (if not already done)
```bash
git add .
git commit -m "Added Streamlit Cloud support"
git push origin main
```

### 2. **Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository: `ZERO-70/Attendence-system`
4. Set main file path: `app.py`
5. Click "Deploy"

### 3. **Add Secrets to Streamlit Cloud**

**IMPORTANT:** Copy the contents from `.streamlit/secrets.toml` to your Streamlit Cloud app secrets:

1. Go to your deployed app dashboard
2. Click "⚙️ Settings" → "Secrets" 
3. Copy and paste the entire contents of `.streamlit/secrets.toml`
4. Click "Save"

### 4. **Required Dependencies**

Make sure you have a `requirements.txt` file with:
```
streamlit>=1.28.0
gspread>=5.10.0
google-auth>=2.22.0
pandas>=2.0.0
```

### 5. **Verify Google Sheets Permissions**

Ensure your Google Sheet is shared with:
- **Email:** `zair-service@inspired-frame-468222-e3.iam.gserviceaccount.com`
- **Permission:** Editor access

## 🔧 Troubleshooting

### Error: "Invalid JWT Signature"
- ✅ **Solution:** Make sure you copied the secrets correctly from `.streamlit/secrets.toml`
- Check that the `private_key` field includes the entire key with line breaks

### Error: "Document not found"
- ✅ **Solution:** Verify the service account email has access to your sheet
- Make sure the sheet name `SE_ATTENDANCE-FALL_2025` is correct

### Error: "No module named gspread"
- ✅ **Solution:** Add `requirements.txt` to your repository root

## 🎯 Local vs Cloud Configuration

The app automatically detects the environment:

- **🏠 Local Development:** Uses `inspired-frame-468222-e3-ca1781f4f058.json` file
- **☁️ Streamlit Cloud:** Uses secrets from `.streamlit/secrets.toml`

## 📱 Features Available on Cloud

✅ Date selection and worksheet management  
✅ Fast Mode with keyboard shortcuts (Q/W/E)  
✅ Large button interface  
✅ Real-time Google Sheets sync  
✅ Responsive design for mobile devices  

## 🔐 Security Notes

- The `.streamlit/secrets.toml` file is for reference only
- Never commit this file to public repositories
- Streamlit Cloud encrypts all secrets
- Service account has minimal required permissions

Your attendance app will be accessible via a URL like:
`https://your-app-name.streamlit.app`

## 🚀 Quick Deploy Checklist

- [ ] Repository pushed to GitHub
- [ ] `requirements.txt` present in root
- [ ] App deployed on Streamlit Cloud  
- [ ] Secrets added from `.streamlit/secrets.toml`
- [ ] Google Sheet shared with service account
- [ ] App tested and working

Happy deploying! 🎉
