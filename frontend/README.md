# Coastal Threat Alert System - Frontend

A modern React dashboard for real-time coastal threat monitoring and alerting, featuring interactive maps, data visualization, and real-time notifications.

## 🚀 Features

- **Interactive Map**: Leaflet.js integration with real-time weather and tide station markers
- **Real-time Alerts**: Live alert display with severity indicators and actions
- **Data Visualization**: Chart.js powered charts for tide, wind, and pressure monitoring
- **Responsive Design**: Mobile-friendly interface built with Tailwind CSS
- **Toast Notifications**: Real-time alerts and status updates
- **Auto-refresh**: Automatic data updates every 30 seconds
- **Mock Data Fallback**: Works offline with simulated data for testing

## 🛠 Tech Stack

- **Framework**: React 18 with functional components and hooks
- **Styling**: Tailwind CSS for rapid UI development
- **Mapping**: Leaflet.js with react-leaflet for interactive maps
- **Charts**: Chart.js with react-chartjs-2 for data visualization
- **Notifications**: react-toastify for toast alerts
- **HTTP Client**: Axios for API communication
- **Build Tool**: Create React App

## 📋 Prerequisites

- Node.js 16+ and npm/yarn
- Backend FastAPI server running (optional - has mock data fallback)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration (Optional)

Create a `.env` file in the frontend directory to configure the backend URL:

```bash
REACT_APP_API_URL=http://localhost:8000
```

If not set, the frontend will default to `http://localhost:8000`.

### 3. Start Development Server

```bash
npm start
```

The application will open at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

## 🎯 Component Architecture

### Core Components

- **MapView**: Interactive Leaflet map with weather/tide stations and alert markers
- **AlertList**: Real-time alert display with severity indicators and actions
- **Charts**: Data visualization for tide, wind, and pressure monitoring
- **Dashboard**: Main layout combining all components with real-time updates

### Key Features

#### Interactive Map
- Real-time weather and tide station markers
- Alert markers with severity-based colors
- Risk zone overlays for high/critical alerts
- Click handlers for location selection
- Coastal boundary visualization

#### Alert Management
- Real-time alert display with severity colors
- Alert deactivation functionality
- Cyclone simulation for testing
- Toast notifications for new alerts
- Alert history and status tracking

#### Data Visualization
- Multi-chart support (Tide, Wind, Pressure)
- Real-time data updates
- Threshold line indicators
- Anomaly point highlighting
- Responsive chart switching

## 🔧 Configuration

### Backend Integration

The frontend automatically detects backend availability:

1. **Connected Mode**: Fetches real data from FastAPI backend
2. **Fallback Mode**: Uses mock data when backend is unavailable
3. **Hybrid Mode**: Combines real and mock data as needed

### API Endpoints

The frontend communicates with these backend endpoints:

- `GET /api/data` - Weather and tide data
- `GET /api/alerts` - Active alerts
- `POST /api/alerts/{id}/deactivate` - Deactivate alerts
- `POST /api/simulate/cyclone` - Simulate cyclone alert

### Mock Data

When the backend is unavailable, the frontend provides realistic mock data:

- **Weather Data**: Simulated temperature, wind, pressure, humidity
- **Tide Data**: Simulated tide heights with natural variations
- **Alerts**: Sample alerts for demonstration

## 🎨 UI/UX Features

### Responsive Design
- Mobile-first approach
- Grid-based layouts that adapt to screen sizes
- Touch-friendly interactions

### Visual Indicators
- Color-coded severity levels (low, medium, high, critical)
- Animated alert markers
- Status indicators for API connections
- Loading states and error handling

### Accessibility
- Semantic HTML structure
- ARIA labels and descriptions
- Keyboard navigation support
- High contrast color schemes

## 🧪 Testing and Development

### Development Features
- Hot reload for rapid development
- Console logging for debugging
- Error boundaries and fallbacks
- Mock data simulation

### Testing Scenarios
- **Backend Connected**: Full functionality with real data
- **Backend Disconnected**: Mock data fallback
- **Network Errors**: Graceful error handling
- **Alert Simulation**: Test cyclone alert generation

## 📱 Mobile Experience

The dashboard is fully responsive and optimized for mobile devices:

- Touch-friendly map interactions
- Swipeable chart navigation
- Collapsible sidebar for alerts
- Mobile-optimized button sizes

## 🔄 Real-time Updates

### Auto-refresh System
- Data updates every 30 seconds
- Alert notifications in real-time
- Status indicators for system health
- Connection monitoring

### Notification System
- Toast notifications for alerts
- Success/error feedback
- Non-intrusive messaging
- Configurable display duration

## 🚨 Alert System

### Alert Types
- **Cyclone**: Critical weather event
- **High Wind**: Wind speed threshold exceeded
- **High Tide**: Tide height threshold exceeded
- **Low Pressure**: Atmospheric pressure below threshold
- **Storm Surge Risk**: Combined high wind and tide conditions

### Severity Levels
- **Low**: Minor threshold exceedance
- **Medium**: Moderate exceedance
- **High**: Significant exceedance
- **Critical**: Severe conditions requiring immediate action

## 📊 Data Visualization

### Chart Types
- **Tide Monitoring**: 24-hour tide height trends
- **Wind Monitoring**: Wind speed patterns
- **Pressure Monitoring**: Atmospheric pressure changes

### Features
- Real-time data plotting
- Threshold line indicators
- Anomaly point highlighting
- Interactive tooltips
- Responsive chart sizing

## 🗺️ Map Features

### Interactive Elements
- Weather station markers (blue)
- Tide station markers (teal)
- Alert markers (color-coded by severity)
- Risk zone overlays
- Coastal boundary visualization

### Map Controls
- Zoom in/out
- Pan navigation
- Marker popups with detailed information
- Click handlers for location selection

## 🔧 Customization

### Styling
- Tailwind CSS classes for easy customization
- CSS custom properties for theme colors
- Responsive breakpoints
- Component-specific styling

### Configuration
- Environment variable support
- API endpoint configuration
- Mock data customization
- Chart options and styling

## 🚀 Deployment

### Build Process
```bash
npm run build
```

### Production Considerations
- Environment variable configuration
- API endpoint URLs
- CDN for static assets
- Performance optimization

### Hosting Options
- Netlify
- Vercel
- AWS S3 + CloudFront
- GitHub Pages

## 🐛 Troubleshooting

### Common Issues

1. **Map Not Loading**
   - Check Leaflet CSS imports
   - Verify map container dimensions
   - Check browser console for errors

2. **Charts Not Rendering**
   - Verify Chart.js dependencies
   - Check data format and structure
   - Ensure proper chart container sizing

3. **API Connection Issues**
   - Verify backend server is running
   - Check CORS configuration
   - Verify API endpoint URLs

4. **Styling Issues**
   - Ensure Tailwind CSS is properly imported
   - Check PostCSS configuration
   - Verify custom CSS imports

### Debug Mode
Enable debug logging by setting:
```javascript
localStorage.setItem('debug', 'true');
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of HackOut'25 hackathon.

## 🆘 Support

For issues and questions:
1. Check the browser console for errors
2. Verify backend connectivity
3. Test with mock data mode
4. Review component documentation

---

**Happy Hacking! 🚀**
