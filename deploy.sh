#!/bin/bash

echo "🚀 Discord Tech News Bot - Complete Rebuild Script"
echo "=================================================="

# Stop and remove existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove old images
echo "🗑️ Removing old images..."
docker rmi discord-tech-news-bot:latest 2>/dev/null || true

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Build fresh image
echo "🔨 Building fresh Docker image..."
docker-compose build --no-cache

# Start the bot
echo "🚀 Starting the bot..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "📋 Check logs with: docker-compose logs -f" 