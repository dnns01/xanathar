import os
from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import polls, appointments

# .env file is necessary in the same directory, that contains several strings.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ACTIVITY = os.getenv('DISCORD_ACTIVITY')

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(dm_help=True)
extensions = ["cogs.appointments", "cogs.polls"]


class Xanathar(commands.Bot):
    def __init__(
            self,
            *args,
            initial_extensions: List[str],
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions

    # async def on_ready(self):
    #     print("Client started!")

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        guild = discord.Object(id=731078161919377499)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


bot = Xanathar(command_prefix='!', help_command=help_command, activity=discord.Game(ACTIVITY), intents=intents,
               initial_extensions=extensions)
bot.run(TOKEN)
