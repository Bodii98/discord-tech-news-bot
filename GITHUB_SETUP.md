# GitHub Repository Setup Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Repository name: `discord-tech-news-bot`
4. Description: `Discord bot that provides tech news in English and Arabic`
5. Make it **Public** (so you can clone it on your server)
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

## Step 2: Push Your Code to GitHub

After creating the repository, GitHub will show you commands. Run these in your project directory:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: Discord Tech News Bot"

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/discord-tech-news-bot.git

# Push to GitHub
git push -u origin main
```

## Step 3: Clone on Your Server

Once the code is on GitHub, you can clone it on your server:

```bash
git clone https://github.com/YOUR_USERNAME/discord-tech-news-bot.git
cd discord-tech-news-bot
```

## Step 4: Set Up Environment Variables

On your server, create the `.env` file:

```bash
cp env.example .env
# Edit .env with your actual tokens
```

## Step 5: Deploy to Portainer

Follow the deployment instructions in README.md

## Important Notes

- The `.env` file is ignored by Git (for security)
- You'll need to create the `.env` file on your server with your real tokens
- The repository is public so others can see your code (but not your tokens) 