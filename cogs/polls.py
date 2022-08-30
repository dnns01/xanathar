import os

from discord.ext import commands

from cogs.components.poll.poll import Poll


class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="poll", pass_context=True, invoke_without_command=True)
    async def cmd_poll(self, ctx, question, *answers):
        """ Create a new poll """

        await Poll(self.bot, question, list(answers), ctx.author.id).send_poll(ctx)

    @cmd_poll.command(name="edit")
    async def cmd_edit_poll(self, ctx, message_id, question, *answers):
        message = await ctx.fetch_message(message_id)
        if message:
            if message.embeds[0].title == "Umfrage":
                old_poll = Poll(self.bot, message=message)
                new_poll = Poll(self.bot, question=question, answers=list(answers), author=old_poll.author)
                await new_poll.send_poll(ctx.channel, message=message)
        else:
            ctx.send("Fehler! Umfrage nicht gefunden!")
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if payload.emoji.name in ["🗑️", "🛑"]:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if len(message.embeds) > 0 and message.embeds[0].title == "Umfrage":
                poll = Poll(self.bot, message=message)
                if str(payload.user_id) == poll.author:
                    if payload.emoji.name == "🗑️":
                        await poll.delete_poll()
                    else:
                        await poll.close_poll()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Polls(bot))
