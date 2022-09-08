import os
from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env file is necessary in the same directory, that contains several strings.
from views import poll_view, appointment_view

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ACTIVITY = os.getenv('DISCORD_ACTIVITY')

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(dm_help=True)
extensions = ["extensions.appointments", "extensions.polls"]


class Xanathar(commands.Bot):
    def __init__(self, *args, initial_extensions: List[str], **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        await self.tree.sync()


bot = Xanathar(command_prefix='!', help_command=help_command, activity=discord.Game(ACTIVITY), intents=intents,
               initial_extensions=extensions)
bot.run(TOKEN)
