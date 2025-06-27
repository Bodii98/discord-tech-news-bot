# Discord Tech News Bot

A Discord bot that provides the latest technology news in English and Arabic using slash commands.

## Features

- `/technews` command with language selection (English/Arabic)
- Fetches real-time tech news from NewsAPI
- Supports both English and Arabic languages
- Automatic command registration and syncing

## Prerequisites

- Discord Bot Token (from Discord Developer Portal)
- NewsAPI Key (from https://newsapi.org/)
- Docker and Docker Compose (for containerized deployment)
- Portainer (for easy container management)

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DISCORD_TOKEN=your_discord_bot_token_here
NEWSAPI_KEY=your_news_api_key_here
```

## Deployment to Portainer

### Method 1: Using Docker Compose (Recommended)

1. **Prepare your environment:**
   - Copy `env.example` to `.env`
   - Fill in your actual Discord token and NewsAPI key in the `.env` file

2. **Upload to your server:**
   - Upload all project files to your server where Portainer is running
   - Make sure the `.env` file is in the same directory as `docker-compose.yml`

3. **Deploy via Portainer:**
   - Open Portainer web interface
   - Go to "Stacks" section
   - Click "Add stack"
   - Give your stack a name (e.g., "discord-bot")
   - Upload the `docker-compose.yml` file or paste its contents
   - Click "Deploy the stack"

4. **Monitor the deployment:**
   - Check the logs in Portainer to ensure the bot starts successfully
   - The bot will automatically restart if it crashes

### Method 2: Using Portainer's Container Creation

1. **Build the image:**
   ```bash
   docker build -t discord-tech-news-bot .
   ```

2. **Create container in Portainer:**
   - Go to "Containers" → "Add container"
   - Name: `discord-tech-news-bot`
   - Image: `discord-tech-news-bot:latest`
   - Add environment variables:
     - `DISCORD_TOKEN`: your_discord_bot_token
     - `NEWSAPI_KEY`: your_news_api_key
   - Set restart policy to "Unless stopped"
   - Deploy the container

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual tokens
   ```

3. **Run the bot:**
   ```bash
   python bot.py
   ```

## Bot Commands

- `/technews [language]` - Get latest tech news
  - `language`: Choose "en" for English or "ar" for Arabic

## Troubleshooting

- **Bot not responding:** Check if the bot token is correct and the bot has proper permissions
- **News not loading:** Verify your NewsAPI key is valid and has remaining requests
- **Container won't start:** Check the logs in Portainer for error messages
- **Commands not syncing:** Ensure the bot has the "applications.commands" scope in Discord

## Security Notes

- Never commit your `.env` file to version control
- Use environment variables for sensitive data
- The Docker container runs as a non-root user for security
- Consider using Docker secrets for production deployments

## Support

If you encounter issues:
1. Check the container logs in Portainer
2. Verify your environment variables are set correctly
3. Ensure your Discord bot has the necessary permissions 