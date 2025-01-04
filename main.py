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
# RUN BOT
# ========================================
# Start bot
@bot.event
async def on_ready():
  await bot.tree.sync()
  print(f"{bot.user} is now running!")

bot.run(token=BOT_KEY)