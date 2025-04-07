# Fact-Forecast Frontend

An interactive web application that visualizes fact-checking articles from around the world using a dynamic map interface. The frontend connects to a FastAPI backend to retrieve article data and presents it in a user-friendly format.

## Project Structure

```
frontend/
├── assets/                  # Static assets like GeoJSON data and images
├── layers/                  # Map layer configurations
├── services/
│   └── api.js               # API service for backend communication
├── .gitignore               # Git ignore file
├── converter.py             # Utility for converting GeoJSON formats
├── countryStyles.js         # Styling for country features on the map
├── customMapView.js         # Custom map view configuration
├── index.html               # Main HTML entry point
├── main.js                  # Application entry point and map initialization
├── package.json             # Project dependencies and scripts
├── storyButtons.js          # UI components for story navigation
├── storyContainer.js        # Component for displaying fact-checking articles
├── style.css                # Application styles
└── vite.config.js           # Vite configuration
```

## Features

- **Interactive World Map**: Clickable countries that highlight on hover
- **Article Display**: Shows fact-checking articles for the selected country
- **Real-time Data**: Fetches the latest articles from the backend API
- **Responsive Design**: Works on desktop and mobile devices
- **Loading Indicators**: Visual feedback during API requests
- **Error Handling**: Graceful handling of API errors
- **Country Mapping**: Intelligent mapping of country names to country codes

## Technology Stack

- **Vanilla JavaScript**: No framework dependencies for simplicity
- **OpenLayers**: For interactive map visualization
- **Vite**: Modern build tool for fast development and optimized production builds
- **Fetch API**: For communication with the backend

## Setup

### Prerequisites

- Node.js (14+)
- npm or yarn
- Backend server running (see backend README)

### Installation

1. Install dependencies:
   ```
   npm install
   ```

### Running the Application

1. Start the development server:
   ```
   npm start
   ```
   This will start the server at http://localhost:5173

2. Make sure the backend server is running at http://localhost:8000

### Building for Production

1. Generate a production build:
   ```
   npm run build
   ```

2. The built files will be in the `dist` directory, which can be deployed to any static hosting service

3. To preview the production build locally:
   ```
   npm run serve
   ```

## API Integration

The frontend communicates with the backend through the API service in `services/api.js`, which provides the following functions:

- `fetchArticlesByCountry(countryCode)`: Retrieves articles for a specific country
- `getCacheStatus()`: Gets the current status of the backend cache
- `refreshCache(countries)`: Triggers a cache refresh for specified countries

## User Interaction Flow

1. User loads the application and sees the world map
2. Hovering over a country highlights it
3. Clicking on a country:
   - Shows a loading indicator
   - Fetches articles for that country from the backend
   - Displays up to 10 most recent articles in the sidebar
4. Each article shows:
   - Title
   - Publication date
   - Source
   - Brief content preview
   - Link to the full article

## Country Code Mapping

The application includes a mapping function in `main.js` that converts country names from the map data to country codes used by the API. This ensures proper communication with the backend regardless of naming differences.

## Error Handling

The frontend implements robust error handling for API requests, including:

- Network errors
- Backend server errors
- Empty article responses
- Invalid country selections

Errors are displayed to the user with helpful messages and suggestions.

## Development Notes

- The map uses GeoJSON data for country boundaries
- Article data is fetched on-demand to minimize loading times
- The application uses a simple caching mechanism to avoid redundant API calls
- Styling is handled through CSS with a mobile-first approach

## Browser Compatibility

The application is compatible with modern browsers including:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)