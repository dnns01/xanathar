import discord
from discord import app_commands, Interaction
from discord.ext import commands

from cogs.components.poll.poll import Poll


@app_commands.guild_only()
class Polls(commands.GroupCog, name="poll", description="Handle Polls in Channels"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="add", description="Erstelle eine Umfrage mit bis zu 20 Antwortmöglichkeiten.")
    @app_commands.describe(question="Welche Frage möchtest du stellen?", choice_a="1. Antwortmöglichkeit",
                           choice_b="2. Antwortmöglichkeit", choice_c="3. Antwortmöglichkeit",
                           choice_d="4. Antwortmöglichkeit", choice_e="5. Antwortmöglichkeit",
                           choice_f="6. Antwortmöglichkeit", choice_g="7. Antwortmöglichkeit",
                           choice_h="8. Antwortmöglichkeit", choice_i="9. Antwortmöglichkeit",
                           choice_j="10. Antwortmöglichkeit", choice_k="11. Antwortmöglichkeit",
                           choice_l="12. Antwortmöglichkeit", choice_m="13. Antwortmöglichkeit",
                           choice_n="14. Antwortmöglichkeit", choice_o="15. Antwortmöglichkeit",
                           choice_p="16. Antwortmöglichkeit", choice_q="17. Antwortmöglichkeit",
                           choice_r="18. Antwortmöglichkeit", choice_s="19. Antwortmöglichkeit",
                           choice_t="20. Antwortmöglichkeit")
    async def cmd_poll(self, interaction: Interaction, question: str, choice_a: str, choice_b: str,
                       choice_c: str = None, choice_d: str = None, choice_e: str = None, choice_f: str = None,
                       choice_g: str = None, choice_h: str = None, choice_i: str = None, choice_j: str = None,
                       choice_k: str = None, choice_l: str = None, choice_m: str = None, choice_n: str = None,
                       choice_o: str = None, choice_p: str = None, choice_q: str = None, choice_r: str = None,
                       choice_s: str = None, choice_t: str = None):
        """ Create a new poll """
        choices = [choice for choice in
                   [choice_a, choice_b, choice_c, choice_d, choice_e, choice_f, choice_g, choice_h, choice_i, choice_j,
                    choice_k, choice_l, choice_m, choice_n, choice_o, choice_p, choice_q, choice_r, choice_s, choice_t]
                   if choice]
        await Poll(self.bot, question, choices, interaction.user.id).send_poll(interaction)
        # view = DropdownView()
        # await ctx.send("", view=view)
        await interaction.response.send_message("")

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


class Dropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Red', description='Your favourite colour is red'),
            discord.SelectOption(label='Green', description='Your favourite colour is green'),
            discord.SelectOption(label='Blue', description='Your favourite colour is blue'),
            discord.SelectOption(label='1', description='Your favourite colour is blue'),
            discord.SelectOption(label='2', description='Your favourite colour is blue'),
            discord.SelectOption(label='3', description='Your favourite colour is blue'),
            discord.SelectOption(label='4', description='Your favourite colour is blue'),
            discord.SelectOption(label='5', description='Your favourite colour is blue'),
            discord.SelectOption(label='7', description='Your favourite colour is blue'),
            discord.SelectOption(label='6', description='Your favourite colour is blue'),
            discord.SelectOption(label='8', description='Your favourite colour is blue'),
            discord.SelectOption(label='9', description='Your favourite colour is blue'),
            discord.SelectOption(label='0', description='Your favourite colour is blue'),
            discord.SelectOption(label='10', description='Your favourite colour is blue'),
            discord.SelectOption(label='11', description='Your favourite colour is blue'),
            discord.SelectOption(label='12', description='Your favourite colour is blue'),
            discord.SelectOption(label='13', description='Your favourite colour is blue'),
            discord.SelectOption(label='14', description='Your favourite colour is blue'),
            discord.SelectOption(label='15', description='Your favourite colour is blue'),
            discord.SelectOption(label='16', description='Your favourite colour is blue'),
            discord.SelectOption(label='17', description='Your favourite colour is blue'),
            discord.SelectOption(label='18', description='Your favourite colour is blue'),
            discord.SelectOption(label='19', description='Your favourite colour is blue'),
            discord.SelectOption(label='20', description='Your favourite colour is blue'),
            discord.SelectOption(label='21', description='Your favourite colour is blue'),

        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())
