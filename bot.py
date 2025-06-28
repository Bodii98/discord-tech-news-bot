import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

# Validate required environment variables
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is required")
if not NEWSAPI_KEY:
    raise ValueError("NEWSAPI_KEY environment variable is required")

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class TechNewsBot:
    def __init__(self):
        self.bot = bot
        self.setup_commands()
    
    def setup_commands(self):
        """Setup slash commands"""
        
        @self.bot.tree.command(
            name="technews",
            description="Get the latest technology news in English or Arabic"
        )
        @app_commands.describe(
            language="Choose language: en (English) or ar (Arabic)"
        )
        async def technews(interaction: discord.Interaction, language: str):
            """Get latest technology news"""
            await self.handle_technews(interaction, language)
        
        # Add autocomplete for language selection
        @technews.autocomplete('language')
        async def language_autocomplete(interaction: discord.Interaction, current: str):
            choices = [
                app_commands.Choice(name="English", value="en"),
                app_commands.Choice(name="Arabic", value="ar")
            ]
            return [choice for choice in choices if current.lower() in choice.name.lower()]
    
    async def handle_technews(self, interaction: discord.Interaction, language: str):
        """Handle the technews command"""
        
        # Validate language parameter
        if language not in ["en", "ar"]:
            await interaction.response.send_message(
                "❌ Please choose 'en' for English or 'ar' for Arabic.",
                ephemeral=True
            )
            return
        
        # Defer response to show typing indicator
        await interaction.response.defer()
        
        try:
            # Fetch news from NewsAPI
            url = f"https://newsapi.org/v2/top-headlines"
            params = {
                "category": "technology",
                "language": language,
                "apiKey": NEWSAPI_KEY,
                "pageSize": 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                await interaction.followup.send(
                    "❌ Failed to fetch news. Please try again later.",
                    ephemeral=True
                )
                return
            
            data = response.json()
            articles = data.get("articles", [])
            
            if not articles:
                await interaction.followup.send(
                    "📰 No technology news found at the moment.",
                    ephemeral=True
                )
                return
            
            # Create main embed
            main_embed = discord.Embed(
                title="📰 Latest Technology News",
                description=f"Top technology news in {'English' if language == 'en' else 'Arabic'}",
                color=0x00ff00,
                url="https://newsapi.org"
            )
            
            # Get the first article for main embed thumbnail
            first_article = articles[0]
            thumbnail_url = first_article.get("urlToImage")
            if thumbnail_url:
                main_embed.set_thumbnail(url=thumbnail_url)
            
            # Add first article to main embed
            title = first_article.get("title", "No title")
            url = first_article.get("url", "")
            description = first_article.get("description", "")
            
            # Truncate description if too long
            if description and len(description) > 200:
                description = description[:200] + "..."
            
            field_value = description if description else "No description available"
            if url:
                field_value += f"\n[Read More]({url})"
            
            main_embed.add_field(
                name=f"🔥 {title}",
                value=field_value,
                inline=False
            )
            
            # Add footer
            main_embed.set_footer(text="Powered by NewsAPI • Use /technews to get more news")
            
            # Send main embed
            await interaction.followup.send(embed=main_embed)
            
            # Create additional embeds for remaining articles (if any)
            for i, article in enumerate(articles[1:3], 2):
                title = article.get("title", "No title")
                url = article.get("url", "")
                description = article.get("description", "")
                image_url = article.get("urlToImage")
                
                # Create embed for each article
                article_embed = discord.Embed(
                    title=f"📰 {title}",
                    description=description[:300] + "..." if description and len(description) > 300 else description,
                    color=0x00ff00,
                    url=url if url else None
                )
                
                # Add image if available
                if image_url:
                    article_embed.set_image(url=image_url)
                
                # Add source and timestamp
                source = article.get("source", {}).get("name", "Unknown Source")
                published_at = article.get("publishedAt", "")
                if published_at:
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                        article_embed.set_footer(text=f"Source: {source} • {dt.strftime('%B %d, %Y')}")
                    except:
                        article_embed.set_footer(text=f"Source: {source}")
                else:
                    article_embed.set_footer(text=f"Source: {source}")
                
                await interaction.followup.send(embed=article_embed)
            
        except requests.RequestException as e:
            print(f"Network error: {e}")
            await interaction.followup.send(
                "❌ Network error. Please try again later.",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error in technews command: {e}")
            await interaction.followup.send(
                "❌ An error occurred. Please try again later.",
                ephemeral=True
            )

# Create bot instance
tech_bot = TechNewsBot()

@bot.event
async def on_ready():
    """Called when bot is ready"""
    print(f"🤖 Bot logged in as {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id if bot.user else 'Unknown'}")
    print(f"📡 Connected to {len(bot.guilds)} server(s)")
    
    try:
        # Sync commands globally
        print("🔄 Syncing slash commands...")
        synced = await bot.tree.sync()
        print(f"✅ Successfully synced {len(synced)} command(s) globally")
        print("🚀 Bot is ready and online!")
        
        # Set bot status
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="/technews for latest tech news"
            )
        )
        
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@bot.event
async def on_guild_join(guild):
    """Called when bot joins a new server"""
    print(f"🎉 Joined new server: {guild.name} (ID: {guild.id})")
    
    try:
        # Sync commands for the new server
        await bot.tree.sync(guild=guild)
        print(f"✅ Synced commands for {guild.name}")
    except Exception as e:
        print(f"❌ Error syncing commands for {guild.name}: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Command error: {error}")

async def main():
    """Main function"""
    print("🚀 Starting Discord Tech News Bot...")
    print("📋 Features:")
    print("   • Global slash commands")
    print("   • English and Arabic news")
    print("   • Beautiful embed messages with images")
    print("   • Auto-sync for new servers")
    
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 