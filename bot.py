import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

# Validate environment variables
assert DISCORD_TOKEN is not None, "DISCORD_TOKEN environment variable is required"
assert NEWSAPI_KEY is not None, "NEWSAPI_KEY environment variable is required"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class TechNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="technews", description="Get the latest tech news in English or Arabic.")
    @app_commands.describe(language="Choose the language: en (English) or ar (Arabic)")
    async def technews(self, interaction: discord.Interaction, language: str):
        if language not in ["en", "ar"]:
            await interaction.response.send_message("Please choose 'en' for English or 'ar' for Arabic.", ephemeral=True)
            return
        url = (
            f"https://newsapi.org/v2/top-headlines?category=technology&language={language}&apiKey={NEWSAPI_KEY}"
        )
        response = requests.get(url)
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch news. Please try again later.", ephemeral=True)
            return
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            await interaction.response.send_message("No tech news found.", ephemeral=True)
            return
        # Limit to top 3 articles
        news_list = []
        for article in articles[:3]:
            title = article.get("title", "No title")
            url = article.get("url", "")
            news_list.append(f"[{title}]({url})")
        news_message = "\n".join(news_list)
        await interaction.response.send_message(f"**Latest Tech News:**\n{news_message}")

    @technews.autocomplete('language')
    async def language_autocomplete(self, interaction: discord.Interaction, current: str):
        languages = [
            app_commands.Choice(name="English", value="en"),
            app_commands.Choice(name="Arabic", value="ar")
        ]
        return [l for l in languages if current.lower() in l.name.lower() or current.lower() in l.value]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        # Clear existing commands first
        bot.tree.clear_commands(guild=None)
        print("Cleared existing commands")
        
        # Add the cog (this will register the command)
        await bot.add_cog(TechNews(bot))
        print("Added TechNews cog")
        
        # Sync commands
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) globally")
        print("Bot is ready!")
    except Exception as e:
        print(f"Error during setup: {e}")

async def main():
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 