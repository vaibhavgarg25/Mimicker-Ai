# Mimicker AI

A full-stack application that automatically analyzes instructional videos and performs browser automation tasks. Upload a video showing how to perform a task, and Mimicker AI will extract the steps and automate them for you.

## 🚀 Features

- **Video Upload & Analysis**: Upload instructional videos and automatically extract automation steps
- **Browser Automation**: Execute extracted steps using Playwright browser automation
- **Real-time Status**: Track analysis and execution progress in real-time
- **User Authentication**: Secure user accounts and video management
- **MCP Integration**: Uses Model Context Protocol for AI-powered video analysis

## 🏗️ Architecture

- **Frontend**: Next.js with TypeScript and Tailwind CSS (Port 3000)
- **Backend**: Flask API with MongoDB (Port 8000)
- **MCP Server**: Video analysis and browser automation service (Port 8080)
- **AI**: Google Gemini for video analysis and step extraction

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- MongoDB (local or cloud)
- Google Gemini API key

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Mimicker-Ai
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file in backend directory:
```env
MONGODB_URI=mongodb://localhost:27017/mimicker_ai
JWT_SECRET_KEY=your-super-secret-jwt-key-here
MCP_SERVER_URL=http://localhost:8080
```

### 3. MCP Server Setup
```bash
cd MCP_server/MCP_mimic
pip install -r requirements.txt
```

Create `.env` file in MCP_server/MCP_mimic directory:
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### 4. Frontend Setup
```bash
cd client
npm install
```

### 5. Database Setup
Make sure MongoDB is running on your system. The application will create the necessary collections automatically.

## 🚀 Running the Application

### Option 1: Run All Services (Windows)
```bash
# Run this from the root directory
start_all.bat
```

### Option 2: Run Services Individually

**Terminal 1 - MCP Server:**
```bash
cd MCP_server/MCP_mimic
python main.py
```

**Terminal 2 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 3 - Frontend:**
```bash
cd client
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **MCP Server**: http://localhost:8080 (internal)

## 📱 How to Use

1. **Sign Up/Login**: Create an account or login at the frontend
2. **Upload Video**: Upload an instructional video (MP4, MOV, AVI, MKV)
3. **Auto Analysis**: The system automatically analyzes your video and extracts steps
4. **View Status**: Check the automation status in your dashboard
5. **Execute Automation**: Start browser automation when analysis is complete
6. **Monitor Progress**: Watch real-time execution logs and status

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - User login
- `POST /api/auth/forgot-password` - Password reset
- `POST /api/auth/reset-password` - Reset password

### Videos
- `POST /api/videos/upload` - Upload video (auto-triggers analysis)
- `GET /api/videos/my-videos` - Get user's videos
- `GET /api/videos/<video_id>` - Get video details

### Automation
- `POST /api/automation/trigger/<video_id>` - Trigger automation
- `GET /api/automation/status/<video_id>` - Get automation status
- `GET /api/automation/results/<video_id>` - Get detailed results
- `GET /api/automation/health` - Check service health

## 🧪 Testing

### Test MCP Server
```bash
cd MCP_server/MCP_mimic
python test_mcp_server.py
```

### Test Video Analysis
```bash
cd MCP_server/MCP_mimic
python test_video_analysis.py
```

## 🔍 Troubleshooting

### Common Issues

1. **MCP Server Connection Failed**
   - Ensure MCP server is running on port 8080
   - Check if Gemini API key is set correctly

2. **Database Connection Error**
   - Verify MongoDB is running
   - Check MONGODB_URI in .env file

3. **Video Analysis Fails**
   - Ensure Gemini API key is valid
   - Check video file format and size

4. **Browser Automation Fails**
   - Install required browser dependencies
   - Check if target website is accessible

### Logs
- Backend logs: Console output from Flask app
- MCP Server logs: Console output from MCP server
- Frontend logs: Browser developer console

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue in the repository