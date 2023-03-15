
from twitchio.ext import commands


class db_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def event_ready(self):
        print("DB cog ready")

    @commands.command(name="db")
    async def db(self, ctx: commands.Context):
        await ctx.send("DB cog")
