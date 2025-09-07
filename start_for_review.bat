@echo off
echo ========================================
echo   MIMICKER AI - PROJECT REVIEW SETUP
echo ========================================
echo.
echo Starting all services for project review...
echo.

echo [1/3] Starting MCP Server (AI Analysis Engine)...
start "MCP Server - AI Analysis" cmd /k "cd MCP_server\MCP_mimic && echo MCP Server Starting... && python main.py"

timeout /t 5 /nobreak > nul

echo [2/3] Starting Backend API...
start "Backend API" cmd /k "cd backend && echo Backend API Starting... && python app.py"

timeout /t 5 /nobreak > nul

echo [3/3] Starting Frontend Application...
start "Frontend App" cmd /k "cd client && echo Frontend Starting... && npm run dev"

timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo   ALL SERVICES STARTED FOR REVIEW!
echo ========================================
echo.
echo Access Points:
echo   Frontend App:  http://localhost:3000
echo   Backend API:   http://localhost:8000  
echo   MCP Server:    http://localhost:8080
echo.
echo Testing Integration...
timeout /t 5 /nobreak > nul

python test_complete_integration.py

echo.
echo Ready for Project Review!
echo Press any key to run demo script...
pause > nul

python demo_for_review.py

echo.
echo Project Review Complete!
pause