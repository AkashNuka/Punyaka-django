#!/bin/bash

# Punyaka MVP - Startup Script

echo "🕉️  Starting Punyaka MVP..."
echo "================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

echo "✓ Docker is running"

# Build and start containers
echo ""
echo "📦 Building and starting containers..."
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "================================"
echo "✅ Punyaka MVP is starting up!"
echo ""
echo "🌐 Access the application at:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000/api"
echo "   Admin:     http://localhost:8000/admin"
echo "   API Docs:  http://localhost:8000/api/swagger/"
echo ""
echo "👤 Demo Login Credentials:"
echo "   Admin:     admin@punyaka.com / admin123"
echo "   Priest:    priest1@punyaka.com / priest123"
echo "   Customer:  customer1@punyaka.com / customer123"
echo ""
echo "📋 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo "================================"
