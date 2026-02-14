#!/bin/bash

echo "🚀 Setting up Pro Prime Series Systems Website..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
cd backend
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Create database
echo "🗄️ Creating database..."
python seed.py

# Start backend in background
echo "🚀 Starting backend server..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Setup frontend
echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install

# Start frontend
echo "🚀 Starting frontend server..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Setup complete!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait