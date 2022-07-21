import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import polls, appointments

# .env file is necessary in the same directory, that contains several strings.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ACTIVITY = os.getenv('DISCORD_ACTIVITY')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', help_command=None, activity=discord.Game(ACTIVITY), intents=intents)



@bot.event
async def on_ready():
    print("Client started!")
    await bot.add_cog(polls.Polls(bot))
    await bot.add_cog(appointments.Appointments(bot))

bot.run(TOKEN)
