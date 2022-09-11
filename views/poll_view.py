import discord

from models import Poll, PollChoiceChosen


class PollView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Abstimmen', style=discord.ButtonStyle.green, custom_id='poll_view:vote', emoji="✅")
    async def vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        poll = Poll.select().where(Poll.message == interaction.message.id)
        if poll:
            poll = poll[0]
            await interaction.response.send_message(f"{poll.question}\n\n*(Nach der Abstimmung kannst du diese Nachricht "
                                                    f"verwerfen. Wenn die Abstimmung nicht funktioniert, bitte verwirf "
                                                    f"die Nachricht und Klicke erneut auf den Abstimmen Button der "
                                                    f"Abstimmung.)*", view=PollChoiceView(poll, interaction.user),
                                                    ephemeral=True)

    @discord.ui.button(label='Beenden', style=discord.ButtonStyle.gray, custom_id='poll_view:close', emoji="🛑")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False)
        poll = Poll.select().where(Poll.message == interaction.message.id)
        if poll:
            poll = poll[0]
            if interaction.user.id == poll.author:
                poll.delete_instance(recursive=True)
                await interaction.edit_original_message(view=None)

    @discord.ui.button(label='Löschen', style=discord.ButtonStyle.gray, custom_id='poll_view:delete', emoji="🗑")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False)
        poll = Poll.select().where(Poll.message == interaction.message.id)
        if poll:
            poll = poll[0]
            if interaction.user.id == poll.author:
                poll.delete_instance(recursive=True)
                await interaction.message.delete()


class PollChoiceView(discord.ui.View):
    def __init__(self, poll, user):
        super().__init__(timeout=None)
        self.poll = poll
        self.user = user
        # Adds the dropdown to our view object.
        self.add_item(PollDropdown(poll, user))


class PollDropdown(discord.ui.Select):
    def __init__(self, poll, user):
        self.poll = poll
        self.user = user
        # Set the options that will be presented inside the dropdown

        options = [discord.SelectOption(label=choice.text, emoji=choice.emoji,
                                        default=len(choice.choice_chosen.filter(member_id=user.id)) > 0) for choice in
                   poll.choices]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Wähle weise....', min_values=0, max_values=len(options), options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)
        for choice in self.poll.choices:
            chosen = choice.choice_chosen.filter(member_id=self.user.id)
            if chosen and choice.text not in self.values:
                chosen[0].delete_instance()
            elif not chosen and choice.text in self.values:
                PollChoiceChosen.create(poll_choice_id=choice.id, member_id=self.user.id)

        message = await interaction.channel.fetch_message(self.poll.message)
        await message.edit(embed=self.poll.get_embed(), view=PollView())
