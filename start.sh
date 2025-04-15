#!/bin/bash

# Get platform
OS=$(uname)

if [[ "$OS" == "Darwin" ]]; then
  echo "Running on macOS..."

  # Frontend
  echo "Starting frontend..."
  cd frontend
  npm start &
  FRONTEND_PID=$!
  cd ..

  # Backend
  echo "Starting backend..."
  cd backend
  source venv/bin/activate
  python main.py

  # Kill frontend on exit
  kill $FRONTEND_PID

elif [[ "$OS" == "Linux" && "$WSL_DISTRO_NAME" != "" ]]; then
  echo "Running on Windows Subsystem for Linux..."

  cd frontend
  npm start &
  FRONTEND_PID=$!
  cd ..

  cd backend
  source venv/bin/activate
  python main.py

  kill $FRONTEND_PID

else
  echo "Running on Windows (native cmd or PowerShell)..."

  # Start frontend
  start cmd /k "cd frontend && npm start"

  # Start backend
  start cmd /k "cd backend && venv\\Scripts\\activate && python main.py"
fi

