from asyncpg import Record
from twitchio.ext import commands

from cogs import toggle


class db_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def event_ready(self):
        print("DB cog ready")

    @commands.command(name="db")
    async def db(self, ctx: commands.Context):
        await ctx.send("DB cog")

    @toggle
    @commands.command(name="dbtest")
    async def dbtest(self, ctx: commands.Context):
        print("dbtest")
        async with self.bot.pool.acquire() as con:
            result: Record = await con.fetch("SELECT COUNT(*) from users;")
            print(result[0]["count"])
            await ctx.send(str(result[0]["count"]))


def prepare(bot: commands.Bot):
    # Load our cog with this module...
    bot.add_cog(db_cog(bot))
