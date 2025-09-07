@echo off
echo 🚀 Mimicker AI Setup Script
echo.

echo 📋 Checking configuration...
python check_config.py

echo.
echo 📦 Installing dependencies...

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo Installing MCP server dependencies...
cd MCP_server\MCP_mimic
pip install -r requirements.txt
cd ..\..

echo Installing frontend dependencies...
cd client
npm install
cd ..

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Copy .env.example files and add your API keys
echo 2. Make sure MongoDB is running
echo 3. Run: start_all.bat
echo.
pause