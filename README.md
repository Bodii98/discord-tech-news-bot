# Discord Tech News Bot

A modern Discord bot that provides the latest technology news in English and Arabic using slash commands.

## ✨ Features

- `/technews` command with language selection (English/Arabic)
- Beautiful embed messages with article descriptions
- Real-time tech news from NewsAPI
- Autocomplete for language selection
- Global command registration
- Robust error handling
- Health checks for container monitoring

## 🚀 Quick Start

### Prerequisites

- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))
- NewsAPI Key (from [NewsAPI.org](https://newsapi.org/))
- Docker and Docker Compose
- Portainer (optional, for easy management)

### 1. Environment Setup

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token_here
NEWSAPI_KEY=your_news_api_key_here
```

### 2. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token to your `.env` file
5. Enable these bot permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Embed Links
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot` and `applications.commands`
8. Select bot permissions: `Send Messages`, `Use Slash Commands`, `Read Message History`, `Embed Links`
9. Use the generated URL to invite the bot to your server

### 3. Deployment

#### Option A: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/Bodii98/discord-tech-news-bot.git
cd discord-tech-news-bot

# Set up environment variables
cp env.example .env
# Edit .env with your tokens

# Deploy with Docker Compose
docker-compose up -d
```

#### Option B: Portainer

1. Upload all files to your server
2. In Portainer, go to "Stacks"
3. Click "Add stack"
4. Name: `discord-bot`
5. Upload `docker-compose.yml` or paste its contents
6. Click "Deploy the stack"

#### Option C: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your tokens

# Run the bot
python bot.py
```

## 📋 Bot Commands

- `/technews [language]` - Get latest technology news
  - `language`: Choose "en" for English or "ar" for Arabic
  - Returns top 3 articles with descriptions and links

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_TOKEN` | Your Discord bot token | Yes |
| `NEWSAPI_KEY` | Your NewsAPI key | Yes |

### Docker Configuration

The bot runs in a container with:
- Non-root user for security
- Health checks every 30 seconds
- Automatic restart on failure
- Volume mounting for logs

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if the bot token is correct
   - Verify the bot has proper permissions
   - Check container logs: `docker logs discord-tech-news-bot`

2. **Commands not appearing**
   - Wait up to 1 hour for global command propagation
   - Ensure the bot has "applications.commands" scope
   - Check if the bot is online

3. **News not loading**
   - Verify your NewsAPI key is valid
   - Check if you have remaining API requests
   - Check network connectivity

4. **Container won't start**
   - Verify environment variables are set
   - Check Docker logs for errors
   - Ensure ports are not in use

### Logs

View container logs:
```bash
docker logs discord-tech-news-bot
```

Or in Portainer:
1. Go to your container
2. Click "Logs" tab

## 🔄 Updates

To update the bot:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the container logs
3. Verify your environment variables
4. Ensure your Discord bot has the necessary permissions

---

**Made with ❤️ for the Discord community** 