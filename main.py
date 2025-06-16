from decouple import config

from discord import Intents, Client, app_commands
from discord.ext import commands, tasks    # pip install discord-ext-bot
import discord   # pip install discord

BOT_KEY = config('BOT_KEY')

# Bot Constants
intents = Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None) # Initialize bot

# ========================================
# ! COMMANDS
# ========================================
# Simple example command
@bot.command(name='hello') # Activate using !hello
async def hello_command(ctx):
  await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command(name='help') # Help command
async def help_command(ctx):
  embed = discord.Embed(
    color=discord.Color.red()
  )
  # Add fields to the embed (optional)
  embed.set_author(
    name="King Bob's Commands",
    url="https://github.com/GabeDiniz",
    # icon_url="<IMAGE-URL>"
  )
  # embed.set_thumbnail(url="<IMAGE-URL>")
  embed.add_field(name='List commands', value='`!help`', inline=False)

  # Send the embed message to the same channel where the command was issued
  await ctx.channel.send(embed=embed)

# ========================================
# SLASH COMMANDS
# ========================================
from datetime import datetime, timedelta, timezone

async def create_event(ctx: discord.Interaction, date: str, time: str, description: str):
  # Parse date and time into a datetime object
  event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
  # Manually set the timezone to EST
  est = timezone(timedelta(hours=-5))
  event_datetime = event_datetime.replace(tzinfo=est)

  # Create event
  event = await ctx.guild.create_scheduled_event(
    name="New Event",
    description=description,
    start_time=event_datetime,
    end_time=event_datetime + timedelta(hours=2),  # Optional: set an appropriate end time
    entity_type=discord.EntityType.external,
    location="Discord",  # Change this to the actual location if needed
    privacy_level=discord.PrivacyLevel.guild_only  # Set the privacy level to guild only
  )
  await ctx.response.send_message(f"Event created! Check it out [here]({event.url})")

# #####################
@bot.tree.command(name="event", description="Create an event", guild=None)
@app_commands.describe(date="Date of the event (YYYY-MM-DD)", time="Event time (HH:MM, 24-hour format)", description="Description of event")
async def create_event(interaction: discord.Interaction, date: str, time: str, description: str):
  await create_event(interaction, date, time, description)

# ========================================
# RUN BOT
# ========================================
# Start bot
@bot.event
async def on_ready():
  await bot.tree.sync()
  print(f"{bot.user} is now running!")

bot.run(token=BOT_KEY)
