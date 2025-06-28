import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

# Validate environment variables
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is required")
if not NEWSAPI_KEY:
    raise ValueError("NEWSAPI_KEY environment variable is required")

# Create bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class TechNewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="technews", description="Get the latest technology news")
    @app_commands.describe(language="Choose language: en (English) or ar (Arabic)")
    async def technews(self, interaction: discord.Interaction, language: str):
        """Get the latest technology news in English or Arabic"""
        
        # Validate language parameter
        if language not in ["en", "ar"]:
            await interaction.response.send_message(
                "Please choose 'en' for English or 'ar' for Arabic.", 
                ephemeral=True
            )
            return

        # Show typing indicator
        await interaction.response.defer()

        try:
            # Fetch news from NewsAPI
            url = f"https://newsapi.org/v2/top-headlines?category=technology&language={language}&apiKey={NEWSAPI_KEY}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                await interaction.followup.send(
                    "Failed to fetch news. Please try again later.", 
                    ephemeral=True
                )
                return

            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                await interaction.followup.send(
                    "No tech news found at the moment.", 
                    ephemeral=True
                )
                return

            # Create news embed
            embed = discord.Embed(
                title="📰 Latest Technology News",
                color=0x00ff00,
                description=f"Top technology news in {'English' if language == 'en' else 'Arabic'}"
            )

            # Add top 3 articles
            for i, article in enumerate(articles[:3], 1):
                title = article.get("title", "No title")
                url = article.get("url", "")
                description = article.get("description", "")[:100] + "..." if article.get("description") else "No description available"
                
                embed.add_field(
                    name=f"{i}. {title}",
                    value=f"{description}\n[Read More]({url})" if url else description,
                    inline=False
                )

            embed.set_footer(text="Powered by NewsAPI")

            await interaction.followup.send(embed=embed)

        except requests.RequestException:
            await interaction.followup.send(
                "Network error. Please try again later.", 
                ephemeral=True
            )
        except Exception as e:
            print(f"Error in technews command: {e}")
            await interaction.followup.send(
                "An error occurred. Please try again later.", 
                ephemeral=True
            )

    @technews.autocomplete('language')
    async def language_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplete for language selection"""
        languages = [
            app_commands.Choice(name="English", value="en"),
            app_commands.Choice(name="Arabic", value="ar")
        ]
        return [lang for lang in languages if current.lower() in lang.name.lower()]

@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f"🤖 Bot logged in as {bot.user}")
    if bot.user:
        print(f"🆔 Bot ID: {bot.user.id}")
    print(f"📡 Connected to {len(bot.guilds)} guild(s)")
    
    try:
        # Sync commands globally
        print("🔄 Syncing commands...")
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s) globally")
        print("🚀 Bot is ready!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Command error: {error}")

async def setup():
    """Setup function to add the cog"""
    await bot.add_cog(TechNewsCog(bot))

async def main():
    """Main function to run the bot"""
    print("🚀 Starting Discord Tech News Bot...")
    
    try:
        # Setup the bot
        await setup()
        
        # Start the bot (DISCORD_TOKEN is validated above)
        await bot.start(DISCORD_TOKEN)  # type: ignore
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 