#!/bin/bash

# Quick setup script for existing environment

echo "🔧 Setting up StudyBuddy with sample data..."

echo "📦 Installing npm dependencies..."
docker-compose exec web npm install

echo "🗃️  Running migrations..."
docker-compose exec web python manage.py migrate

echo "🌱 Seeding database with sample data..."
docker-compose exec web python manage.py seed_db

echo "🎨 Building CSS..."
docker-compose exec web npm run build-once

echo "✅ Setup complete!"
echo ""
echo "🌐 Django app: http://localhost:8000"
echo "🔧 Admin panel: http://localhost:8000/admin"
echo "👤 Admin login: admin@studybuddy.com / admin123"
echo ""
echo "Sample users (all with password 'password123'):"
echo "  - alice@example.com"
echo "  - bob@example.com" 
echo "  - carol@example.com"
echo "  - david@example.com"
echo "  - emma@example.com"
