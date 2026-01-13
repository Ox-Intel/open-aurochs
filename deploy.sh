#!/bin/bash

# Deployment script for DigitalOcean or similar VPS
# Run this on your server after cloning the repository

set -e

echo "🚀 Starting deployment..."

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "❌ .env.production file not found!"
    echo "Please copy .env.production.sample to .env.production and configure it."
    exit 1
fi

# Pull latest code (if using git)
echo "📥 Pulling latest code..."
git pull origin main || true

# Build and start containers
echo "🐳 Building Docker images..."
docker compose -f docker-compose.production.yml build

# Run migrations
echo "🗄️ Running database migrations..."
docker compose -f docker-compose.production.yml run --rm web python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
docker compose -f docker-compose.production.yml run --rm web python manage.py collectstatic --noinput

# Restart services
echo "♻️ Restarting services..."
docker compose -f docker-compose.production.yml down
docker compose -f docker-compose.production.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
docker compose -f docker-compose.production.yml ps

echo "✅ Deployment complete!"
echo "🌐 Application should be available at http://your-server-ip"
echo ""
echo "📝 Next steps:"
echo "1. Configure your domain DNS to point to this server"
echo "2. Set up SSL certificates (consider using Certbot with Let's Encrypt)"
echo "3. Configure firewall rules (ports 80, 443)"
echo "4. Set up monitoring and backups"