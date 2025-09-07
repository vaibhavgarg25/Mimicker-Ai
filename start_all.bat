@echo off
echo Starting Mimicker AI Full Stack...
echo.

echo Starting MCP Server...
start "MCP Server" cmd /k "cd MCP_server\MCP_mimic && python main.py"

timeout /t 3 /nobreak > nul

echo Starting Backend...
start "Backend" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend" cmd /k "cd client && npm run dev"

echo.
echo All services started!
echo - MCP Server: http://localhost:8080
echo - Backend API: http://localhost:8000  
echo - Frontend: http://localhost:3000 (Next.js)
echo.
pause