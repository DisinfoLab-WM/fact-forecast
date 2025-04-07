# Fact Forecast - Global Fact-Checking Tracker

A comprehensive web application that visualizes fact-checking articles from around the world using an interactive map interface. This project was developed by the DisinfoLab engineering team for Spring 2025.

![Fact Forecast Screenshot](https://via.placeholder.com/800x450.png?text=Fact+Forecast+Screenshot)

## Project Overview

Fact Forecast combines a modern frontend with a robust backend to create a tool for tracking and visualizing fact-checking efforts globally:

- **Interactive Map**: Click on countries to view their fact-checking articles
- **Real-time Data**: Fetches the latest articles from a Firebase database
- **Intelligent Caching**: Minimizes database reads while keeping content fresh
- **User-friendly Interface**: Clean design with intuitive navigation

## Project Structure

The project is divided into two main components:

```
fact-forecast/
├── backend/               # FastAPI backend with Firebase integration
├── frontend/              # JavaScript frontend with OpenLayers map
├── data/                  # Shared data resources
└── README.md              # This file
```

Each component has its own README with detailed documentation.

## Features

### Frontend
- Interactive world map with country selection
- Article display with title, source, date, and preview
- Loading indicators and error handling
- Responsive design for desktop and mobile

### Backend
- FastAPI application with Firebase integration
- Intelligent caching system to minimize database reads
- RESTful API endpoints for article retrieval
- Comprehensive logging and error handling

## Technology Stack

- **Frontend**: Vanilla JavaScript, OpenLayers, Vite
- **Backend**: Python, FastAPI, Firebase Realtime Database
- **Data Storage**: Firebase for articles, JSON for caching
- **Deployment**: Local development with potential for cloud deployment

## Getting Started

### Prerequisites

- Node.js (14+) for the frontend
- Python (3.8+) for the backend
- Firebase project with Realtime Database

### Setup and Installation

1. **Clone the repository**
   ```
   git clone https://github.com/DisinfoLab-WM/fact-forecast.git
   cd fact-forecast
   ```

2. **Backend Setup**
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Create a `.env` file in the backend directory with your Firebase credentials:
   ```
   FIREBASE_API_KEY=your_api_key
   FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   FIREBASE_DATABASE_URL=https://your_project.firebaseio.com
   FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
   ```

3. **Frontend Setup**
   ```
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the Backend**
   ```
   cd backend
   python main.py
   ```
   The backend will run at http://localhost:8000

2. **Start the Frontend**
   ```
   cd frontend
   npm start
   ```
   The frontend will run at http://localhost:5173

3. **Access the Application**
   Open your browser and navigate to http://localhost:5173

## API Documentation

Once the backend is running, you can access the API documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Development Workflow

1. The frontend makes API requests to the backend when a country is selected
2. The backend checks its cache for articles from that country
3. If cached data exists and is recent, it returns that data
4. If not, it fetches data from Firebase and updates the cache
5. The frontend displays the articles in a user-friendly format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DisinfoLab for project support and guidance
- OpenLayers for the interactive mapping library
- FastAPI for the efficient backend framework
- Firebase for the flexible database solution
