from twitchio.ext import commands


class ToggleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_toggle = {}  # Dictionary to store command toggle state

    def is_command_enabled(self, command, channel):
        if channel in self.command_toggle:
            return self.command_toggle[channel].get(command, True)
        return True

    def toggle_command(self, command_name, channel):
        if channel not in self.command_toggle:
            self.command_toggle[channel] = {}

        command_state = self.command_toggle[channel].get(command_name, True)
        self.command_toggle[channel][command_name] = not command_state

        if self.command_toggle[channel][command_name]:
            return f"Enabled '{command_name}' command in {channel}."
        else:
            return f"Disabled '{command_name}' command in {channel}."

    @commands.command(name="toggle")
    async def toggle(self, ctx, command_name):
        channel = ctx.channel.name
        message = self.toggle_command(command_name, channel)
        await ctx.send(message)
