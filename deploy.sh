#!/bin/bash

# Build and deploy with Docker Compose
echo "Building and deploying Pro Prime Series Systems..."

# Stop existing containers
docker-compose down

# Build images
docker-compose build

# Run database migrations
docker-compose run --rm backend alembic upgrade head

# Seed the database
docker-compose run --rm backend python seed.py

# Start services
docker-compose up -d

echo "✅ Deployment complete!"
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Database Admin: http://localhost:8080"