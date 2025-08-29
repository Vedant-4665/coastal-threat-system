#!/bin/bash

echo "🚀 Setting up Coastal Threat Alert System for HackOut'25"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Python and Node.js are available"

# Backend Setup
echo ""
echo "🔧 Setting up Backend (FastAPI)"
echo "--------------------------------"

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file from template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env_example.txt .env
    echo "⚠️  Please edit .env file with your API keys and Firebase credentials"
    echo "📱 Firebase Setup Required:"
    echo "   1. Go to https://console.firebase.google.com/"
    echo "   2. Create a new project or select existing one"
    echo "   3. Enable Cloud Messaging"
    echo "   4. Go to Project Settings > Service Accounts"
    echo "   5. Generate New Private Key and download JSON file"
    echo "   6. Place JSON file in backend/ directory"
    echo "   7. Update FIREBASE_CREDENTIALS_PATH in .env"
else
    echo "✅ .env file already exists"
fi

cd ..

# Frontend Setup
echo ""
echo "🎨 Setting up Frontend (React)"
echo "-------------------------------"

cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env file for frontend
if [ ! -f .env ]; then
    echo "Creating frontend .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
    echo "✅ Frontend .env file created"
else
    echo "✅ Frontend .env file already exists"
fi

cd ..

# Create main README
echo ""
echo "📝 Creating project documentation..."
cat > README.md << 'EOF'
# Coastal Threat Alert System - HackOut'25

An AI-powered coastal threat detection and alerting system built with FastAPI and React, featuring real-time weather monitoring, tide analysis, and machine learning-based anomaly detection.

## 🚀 Quick Start

### Backend (FastAPI)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```
Server will start at: http://localhost:8000

### Frontend (React)
```bash
cd frontend
npm start
```
App will open at: http://localhost:3000

## 📊 API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing
- Simulate cyclone alert: `POST /api/simulate/cyclone`
- Test push notification: `POST /api/notifications/test`
- Health check: `GET /api/health`

## 🔧 Configuration
1. Copy `backend/env_example.txt` to `backend/.env`
2. Add your API keys (OpenWeatherMap, NOAA)
3. Configure Firebase credentials (see Firebase Setup below)
4. Restart the backend server

## 🔥 Firebase Setup (Required for Push Notifications)
1. **Create Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create new project or select existing one
   - Enable Cloud Messaging

2. **Generate Service Account Key**:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Download the JSON file
   - Place it in `backend/` directory
   - Update `FIREBASE_CREDENTIALS_PATH` in `.env`

3. **Configure Environment Variables**:
   ```env
   FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
   FIREBASE_PROJECT_ID=your-project-id
   ```

## 📁 Project Structure
```
├── backend/          # FastAPI backend with ML pipeline
├── frontend/         # React dashboard with real-time updates
├── setup.sh          # Automated setup script
└── README.md         # This file
```

## 🌟 Features
- Real-time weather & tide monitoring
- ML-powered anomaly detection
- Interactive coastal map
- Live alert system
- Data visualization charts
- Push notifications (Firebase FCM)
- Responsive web dashboard

## 🛠 Tech Stack
- **Backend**: FastAPI, SQLAlchemy, scikit-learn, pandas
- **Frontend**: React, Tailwind CSS, Leaflet.js, Chart.js
- **APIs**: OpenWeatherMap, NOAA Tides & Currents
- **ML**: Isolation Forest, statistical forecasting
- **Notifications**: Firebase Cloud Messaging (FCM)

## 🚨 Alert Types
- High wind speed
- High tide levels
- Low atmospheric pressure
- Storm surge risk
- ML-detected anomalies

## 📱 Demo
1. Start both backend and frontend
2. Click "Simulate Cyclone" to test alert system
3. Click "Test Push" to test Firebase notifications
4. View real-time data on interactive map
5. Monitor trends in data visualization charts

## 🔔 Push Notifications
- **Firebase FCM**: Cross-platform push notifications
- **Topic-based**: All devices subscribe to "coastal_alerts"
- **Rich content**: Include alert details and actions
- **High priority**: Immediate delivery for critical alerts
- **Testing**: Use "Test Push" button to verify setup

---

**Happy Hacking! 🚀**
EOF

echo "✅ Project README created"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys and Firebase credentials"
echo "2. Set up Firebase project and download service account JSON"
echo "3. Start backend: cd backend && source venv/bin/activate && python main.py"
echo "4. Start frontend: cd frontend && npm start"
echo ""
echo "🔥 Firebase Setup Required:"
echo "   - Create project at https://console.firebase.google.com/"
echo "   - Enable Cloud Messaging"
echo "   - Download service account key"
echo "   - Update .env file"
echo ""
echo "🌊 Welcome to the Coastal Threat Alert System!"
echo "🚀 Built for HackOut'25 - Happy Hacking!"
