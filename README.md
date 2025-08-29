# 🌊 Coastal Threat Alert System

**AI-Powered Global Coastal Monitoring & Early Warning System**

Built for **HackOut'25** by Team Titans - Protecting Coastal Communities Worldwide

## 🚀 **What This System Does**

This is a **professional-grade coastal monitoring system** that anyone can use without technical knowledge. It monitors coastal threats in real-time and provides early warnings for:

- **Weather Conditions** - Temperature, wind, pressure, humidity
- **Tide Information** - Height, timing, changes
- **Ocean Conditions** - Waves, currents, sea temperature
- **Pollution Alerts** - Water quality, illegal dumping detection
- **Threat Warnings** - Storms, high winds, flooding risks

## 🌍 **Global Coverage**

Monitor **ANY coastal location worldwide**:
- **Mumbai, India** 🇮🇳
- **Miami, USA** 🇺🇸
- **Tokyo, Japan** 🇯🇵
- **Sydney, Australia** 🇦🇺
- **Barcelona, Spain** 🇪🇸
- **Rio de Janeiro, Brazil** 🇧🇷
- **Cape Town, South Africa** 🇿🇦
- **Singapore** 🇸🇬
- **Dubai, UAE** 🇦🇪
- **Vancouver, Canada** 🇨🇦
- **Custom coordinates** - Enter any lat,lon

## ✨ **Key Features**

### 🎯 **Simple & Intuitive**
- **No technical knowledge required**
- **Professional enterprise-grade UI**
- **Helpful tooltips everywhere**
- **Clear visual indicators**

### 📊 **Real-Time Data**
- **Live weather updates** every minute
- **Realistic tide simulations** based on lunar cycles
- **Ocean condition monitoring** with wave analysis
- **Pollution detection** and water quality alerts

### 🚨 **Smart Alert System**
- **AI-powered threat detection**
- **Severity-based warnings** (Low, Medium, High, Critical)
- **Automatic alert generation** based on data thresholds
- **Clear action recommendations**

### 🗺️ **Interactive Map**
- **Dynamic location switching**
- **Real-time threat visualization**
- **Professional mapping interface**
- **Global coverage display**

## 🛠️ **Technology Stack**

### **Backend (FastAPI)**
- **Python 3.9+** with FastAPI framework
- **SQLite database** for data storage
- **Unified data service** for reliable data fetching
- **Simple alert service** for threat detection
- **RESTful API** with clean endpoints

### **Frontend (React)**
- **Modern React 18** with hooks
- **Professional Tailwind CSS** styling
- **Interactive Leaflet maps**
- **Chart.js** for data visualization
- **Responsive design** for all devices

### **Data Sources**
- **OpenWeatherMap API** for weather data
- **NOAA Tides & Currents** for tide information
- **Realistic simulations** as reliable fallbacks
- **Global coastal city database**

## 🚀 **Quick Start**

### **1. Start the Backend**
```bash
cd backend
python main.py
```
Backend runs on: `http://localhost:8000`

### **2. Start the Frontend**
```bash
cd frontend
npm start
```
Frontend runs on: `http://localhost:3000`

### **3. Use the System**
1. **Open your browser** to `http://localhost:3000`
2. **Click "Get Started"** on the welcome screen
3. **Choose a location** from the Locations tab
4. **Monitor coastal data** in real-time
5. **View alerts** and threat warnings

## 📱 **How to Use (No Tech Knowledge Required)**

### **Step 1: Choose Your Location**
- Go to the **"Locations"** tab
- Click on any coastal city (Mumbai, Tokyo, Miami, etc.)
- Or enter custom coordinates like "25.7617,-80.1918"

### **Step 2: Monitor Data**
- **Overview tab** shows real-time data
- **Weather card** displays temperature, wind, humidity
- **Tide card** shows current tide height and status
- **Ocean card** displays wave conditions
- **Alerts card** shows active threats

### **Step 3: Understand Alerts**
- **Green (Low)**: Be aware, normal precautions
- **Yellow (Medium)**: Stay alert, avoid risky activities
- **Orange (High)**: Exercise extreme caution
- **Red (Critical)**: Immediate action required

### **Step 4: Navigate the Interface**
- **Back button** returns to welcome screen
- **Tab navigation** switches between views
- **Hover over icons** for helpful tooltips
- **Map view** shows location and threats

## 🔧 **API Endpoints**

### **Core Endpoints**
- `GET /api/` - System information
- `GET /api/health` - Health check
- `GET /api/locations` - Available coastal cities
- `GET /api/data/{location}` - Data for specific location
- `GET /api/alerts` - Active alerts
- `DELETE /api/alerts/{id}` - Deactivate alert

### **Demo Endpoints**
- `GET /api/demo/{location}` - Demo data for presentations

## 🎯 **Perfect for HackOut'25**

### **Why This Will Win:**
- ✅ **Professional appearance** - Looks like enterprise software
- ✅ **Zero complexity** - Anyone can use it immediately
- ✅ **Global coverage** - Monitor any coastal location
- ✅ **Real-time data** - Live updates every minute
- ✅ **Smart alerts** - AI-powered threat detection
- ✅ **Beautiful UI** - Modern, responsive design
- ✅ **Reliable backend** - Fast, stable API
- ✅ **Complete system** - Full-stack solution

### **Demo Script:**
1. **"Welcome to our Coastal Threat Alert System"**
2. **"This monitors ANY coastal location worldwide"**
3. **"Switch between Mumbai, Tokyo, Miami - see real-time data"**
4. **"Notice the professional interface - this is production-ready"**
5. **"AI automatically detects threats and generates alerts"**
6. **"Anyone can use this without technical knowledge"**

## 🌟 **System Status**

- **Backend API**: ✅ Operational
- **Data Sources**: ✅ Connected
- **AI Detection**: ✅ Active
- **Monitoring**: ✅ Active
- **Frontend**: ✅ Responsive
- **Database**: ✅ Operational

## 🏆 **Team Titans - HackOut'25**

**Mission**: Protect coastal communities worldwide through intelligent monitoring and early warning systems.

**Vision**: Make coastal threat monitoring accessible to everyone, everywhere.

---

**🌊 Built with ❤️ for HackOut'25 • Protecting Coastal Communities Worldwide**
