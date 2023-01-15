import discord
from discord import File

from models import Appointment, Attendee


class AppointmentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Zusagen', style=discord.ButtonStyle.green, custom_id='appointment_view:accept', emoji="👍")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        appointment = Appointment.select().where(Appointment.message == interaction.message.id)
        if appointment:
            appointment = appointment[0]
            attendee = appointment.attendees.filter(member_id=interaction.user.id)
            if attendee:
                await interaction.response.send_message("Du bist bereits Teilnehmerin dieses Termins.",
                                                        ephemeral=True)
                return
            else:
                Attendee.create(appointment=appointment.id, member_id=interaction.user.id)
                await interaction.message.edit(embed=appointment.get_embed())

        await interaction.response.defer(thinking=False)

    @discord.ui.button(label='Absagen', style=discord.ButtonStyle.red, custom_id='appointment_view:decline', emoji="👎")
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        appointment = Appointment.select().where(Appointment.message == interaction.message.id)
        if appointment:
            appointment = appointment[0]
            attendee = appointment.attendees.filter(member_id=interaction.user.id)
            if attendee:
                attendee = attendee[0]
                attendee.delete_instance()
                await interaction.message.edit(embed=appointment.get_embed())
            else:
                await interaction.response.send_message("Du kannst nur absagen, wenn du vorher zugesagt hast.",
                                                        ephemeral=True)
                return

        await interaction.response.defer(thinking=False)

    @discord.ui.button(label='Download .ics', style=discord.ButtonStyle.blurple, custom_id='appointment_view:ics',
                       emoji="📅")
    async def ics(self, interaction: discord.Interaction, button: discord.ui.Button):
        appointment = Appointment.select().where(Appointment.message == interaction.message.id)
        if appointment:
            appointment = appointment[0]
            await interaction.response.send_message("", file=File(appointment.get_ics_file(),
                                                                  filename=f"{appointment.title}_{appointment.uuid}.ics"), ephemeral=True)

    @discord.ui.button(label='Löschen', style=discord.ButtonStyle.gray, custom_id='appointment_view:delete', emoji="🗑")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False)
        appointment = Appointment.select().where(Appointment.message == interaction.message.id)
        if appointment:
            appointment = appointment[0]
            if interaction.user.id == appointment.author:
                appointment.delete_instance(recursive=True)
                await interaction.message.delete()
