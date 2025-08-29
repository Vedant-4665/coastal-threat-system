# Coastal Threat Alert System - Backend

An AI-powered coastal threat detection and alerting system built with FastAPI, featuring real-time weather monitoring, tide analysis, and machine learning-based anomaly detection.

## 🚀 Features

- **Real-time Data Fetching**: OpenWeatherMap API integration for weather data
- **Tide Monitoring**: NOAA Tides & Currents API integration
- **ML-Powered Anomaly Detection**: Isolation Forest algorithm for pattern recognition
- **Rule-based Alerting**: Configurable thresholds for wind, tide, and pressure
- **Push Notifications**: Firebase Cloud Messaging (FCM) for real-time alerts
- **Time-series Forecasting**: Tide level predictions using statistical models
- **SQLite Database**: Lightweight data storage with SQLAlchemy ORM

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite + SQLAlchemy
- **ML Libraries**: scikit-learn, statsmodels
- **APIs**: OpenWeatherMap, NOAA Tides & Currents
- **Notifications**: Firebase Cloud Messaging (FCM)
- **Data Processing**: pandas, numpy

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- API keys for OpenWeatherMap and NOAA (optional)
- Firebase project with service account credentials

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the environment template and configure your API keys:

```bash
cp env_example.txt .env
# Edit .env with your actual API keys
```

**Required Environment Variables:**
- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key
- `NOAA_API_KEY`: Your NOAA API key (optional)
- `FIREBASE_CREDENTIALS_PATH`: Path to your Firebase service account JSON file
- `FIREBASE_PROJECT_ID`: Your Firebase project ID

### 3. Firebase Setup

1. **Create a Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or select existing one
   - Enable Cloud Messaging

2. **Generate Service Account Key**:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Download the JSON file
   - Place it in your project directory
   - Update `FIREBASE_CREDENTIALS_PATH` in `.env`

3. **Configure FCM**:
   - The system will automatically use the default topic "coastal_alerts"
   - Devices can subscribe to this topic to receive notifications

### 4. Run the Application

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 API Endpoints

### Core Endpoints

- `GET /api/data` - Fetch recent weather and tide data
- `GET /api/alerts` - Get all active alerts
- `POST /api/alerts/{alert_id}/deactivate` - Deactivate an alert
- `GET /api/forecast/tides` - Get tide forecasts

### Notification Endpoints

- `POST /api/notifications/test` - Send test push notification
- `POST /api/notifications/subscribe` - Subscribe devices to topic
- `POST /api/notifications/unsubscribe` - Unsubscribe devices from topic
- `GET /api/notifications/status` - Get notification service status

### Testing Endpoints

- `POST /api/simulate/cyclone` - Simulate a cyclone alert
- `GET /api/health` - Health check

### Example Usage

```bash
# Get current data
curl http://localhost:8000/api/data

# Get active alerts
curl http://localhost:8000/api/alerts

# Simulate cyclone alert
curl -X POST http://localhost:8000/api/simulate/cyclone

# Send test notification
curl -X POST http://localhost:8000/api/notifications/test

# Subscribe devices to topic
curl -X POST http://localhost:8000/api/notifications/subscribe \
  -H "Content-Type: application/json" \
  -d '{"tokens": ["device_token_1", "device_token_2"]}'
```

## 🔧 Configuration

### Alert Thresholds

Configure alert sensitivity in your `.env` file:

```env
ALERT_THRESHOLD_WIND_SPEED=25.0      # m/s
ALERT_THRESHOLD_TIDE_HEIGHT=2.5      # meters
ALERT_THRESHOLD_PRESSURE=1000.0      # hPa
```

### Firebase Configuration

```env
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
FIREBASE_PROJECT_ID=your-project-id
```

### Database

The system uses SQLite by default. To use PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost/coastal_threats
```

## 🧪 Testing

### Simulate Alerts

```bash
# Simulate a cyclone alert
curl -X POST http://localhost:8000/api/simulate/cyclone
```

### Test Notifications

```bash
# Send test push notification
curl -X POST http://localhost:8000/api/notifications/test
```

### Mock Data

If API keys are not configured, the system automatically falls back to mock data generation for testing purposes.

## 📈 ML Pipeline

### Anomaly Detection

1. **Rule-based**: Threshold-based detection for wind, tide, and pressure
2. **ML-based**: Isolation Forest algorithm for pattern anomaly detection
3. **Combined Risk**: Multi-factor risk assessment (e.g., high wind + high tide)

### Forecasting

- **Tide Prediction**: Statistical forecasting using moving averages and trend analysis
- **Time Horizon**: Configurable forecast periods (default: 24 hours)

## 🔔 Alert System

### Alert Types

- `high_wind`: Wind speed exceeds threshold
- `high_tide`: Tide height exceeds threshold
- `low_pressure`: Atmospheric pressure below threshold
- `storm_surge_risk`: Combined high wind and tide conditions
- `ml_anomaly`: Machine learning detected pattern anomaly

### Severity Levels

- `low`: Minor threshold exceedance
- `medium`: Moderate exceedance
- `high`: Significant exceedance
- `critical`: Severe conditions requiring immediate action

## 📱 Push Notifications

### Firebase Cloud Messaging

The system uses Firebase Cloud Messaging (FCM) for push notifications:

- **Topic-based messaging**: All devices subscribe to "coastal_alerts" topic
- **Cross-platform support**: Works on Android, iOS, and web
- **Rich notifications**: Includes alert details and actions
- **Automatic retry**: FCM handles delivery retries
- **Analytics**: Track notification delivery and engagement

### Notification Features

- **High priority**: Notifications marked as high priority for immediate delivery
- **Rich content**: Include alert type, severity, location, and description
- **Click actions**: Notifications can open the app to specific alerts
- **Badge counts**: Track unread alerts
- **Sound alerts**: Audio notifications for critical alerts

### Device Management

- **Topic subscription**: Devices automatically subscribe to coastal alerts
- **Token management**: Handle device registration and updates
- **Batch operations**: Subscribe/unsubscribe multiple devices at once

## 📁 Project Structure

```
backend/
├── api/
│   └── routes.py          # FastAPI route definitions
├── db/
│   └── models.py          # Database models and setup
├── services/
│   ├── weather_service.py # OpenWeatherMap integration
│   ├── tide_service.py    # NOAA tide data service
│   ├── alert_service.py   # Alert generation and management
│   └── firebase_service.py # Firebase FCM integration
├── ml/
│   └── anomaly_detector.py # ML pipeline and anomaly detection
├── main.py                # FastAPI application entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔍 Monitoring and Debugging

### Logs

The application logs startup events and errors to console. For production, consider integrating with a proper logging service.

### Database Inspection

```bash
# Connect to SQLite database
sqlite3 coastal_threats.db

# View tables
.tables

# Check recent data
SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 5;
SELECT * FROM alerts WHERE is_active = 1;
```

### Firebase Status

Check Firebase service status:

```bash
curl http://localhost:8000/api/notifications/status
```

## 🚀 Production Deployment

### Environment Variables

- Set `DATABASE_URL` to production database
- Configure proper CORS origins
- Set secure API keys
- Enable proper logging
- Configure Firebase production credentials

### Scaling Considerations

- Replace SQLite with PostgreSQL for production
- Implement Redis for caching
- Add rate limiting
- Set up monitoring and alerting
- Use Firebase production project

### Firebase Production Setup

1. **Create Production Project**: Separate from development
2. **Service Account**: Generate production service account key
3. **Security Rules**: Configure proper FCM security rules
4. **Monitoring**: Enable Firebase Analytics and Crashlytics
5. **Testing**: Test notifications on production devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of HackOut'25 hackathon.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error messages
3. Verify environment variable configuration
4. Test with mock data first
5. Check Firebase project configuration
6. Verify service account credentials

## 🔗 Useful Links

- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [FCM Best Practices](https://firebase.google.com/docs/cloud-messaging/concept-options)

---

**Happy Hacking! 🚀**
