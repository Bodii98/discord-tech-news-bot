# Discord Bot Update Instructions

## Summary of Changes Made
- Updated `bot.py` to register commands globally instead of guild-specific
- Pushed changes to GitHub: https://github.com/Bodii98/discord-tech-news-bot.git

## How to Update Your Docker Container in Portainer

### Method 1: Via Portainer Web Interface (Recommended)
1. Open Portainer in your web browser
2. Go to your discord-bot container
3. Stop the container
4. Delete the container (your data is safe)
5. Recreate the container using the updated code

### Method 2: Via Docker Compose (If you have SSH access to server)
```bash
# Navigate to your project directory
cd /path/to/your/bot

# Pull the latest code from GitHub
git pull origin main

# Rebuild and restart using docker-compose
docker-compose down
docker-compose up --build -d
```

### Method 3: Manual Update in Portainer
1. In Portainer, go to your bot container
2. Click "Recreate" or "Update"
3. Make sure it pulls the latest image or rebuilds from source

## Important Notes
- GitHub updates do NOT automatically sync to Docker containers
- You must manually rebuild/redeploy to get the latest code changes
- After updating, wait up to 1 hour for Discord to propagate global commands
- The bot will now work in ALL servers where it's installed, not just your original server

## What Changed
- Removed hardcoded guild_id
- Changed command registration from guild-specific to global
- Updated sync process to work globally

## After Update
1. Restart your bot container
2. Wait up to 1 hour for Discord to propagate commands
3. Test `/technews` command in new servers

---
**Saved on**: [Current Date]
**GitHub Repo**: https://github.com/Bodii98/discord-tech-news-bot.git 