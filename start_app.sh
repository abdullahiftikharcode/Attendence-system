#!/bin/bash
# Attendance App Startup Script

echo "🚀 Starting Attendance Tracker App..."
echo "📍 Working directory: $(pwd)"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Please run the setup first or check your directory"
    exit 1
fi

# Check if credentials exist
if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found!"
    echo "💡 Please ensure your Google service account credentials are in the current directory"
    exit 1
fi

echo "✅ All requirements found"
echo "🌐 Starting Streamlit app..."
echo ""
echo "📝 Open your browser and go to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the app"
echo ""

# Start the Streamlit app
.venv/bin/python -m streamlit run app.py
