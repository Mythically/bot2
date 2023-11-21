import beckett
import pokepy
import botDB

from asyncio import sleep
from random import randint
from twitchio.ext import commands


class pokedex_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pokemonClient = pokepy.V2Client(cache="in_disk", cache_location="./cache")

    async def get_mon(self, id):
        pokemon = self.pokemonClient.get_pokemon(id)
        return pokemon

    @commands.command(name="mon")
    @commands.cooldown(rate=2, per=30, bucket=commands.Bucket.user)
    async def pokemon(self, ctx) -> None:
        try:
            pokemon_id = randint(0, 1126)
            if pokemon_id > 903:
                await ctx.channel.send(await botDB.getEscapePhrase())
                return
            pokemon = await self.get_mon(pokemon_id)
            pokemon_name = pokemon.forms[0].name
            if "tapu" in pokemon_name:
                link_pokemon_name = pokemon_name
            else:
                link_pokemon_name = pokemon_name.split("-")
            link_pokemon_name = (
                str(link_pokemon_name[0]).strip("[").strip("]").strip("'")
            )
            link = f"https://pokemondb.net/pokedex/{link_pokemon_name}"
            await botDB.insertCaughtPokemon(
                int(pokemon_id), pokemon_name, int(ctx.author.id), ctx.author.name
            )
            await ctx.channel.send(
                "@"
                + str(ctx.author.name)
                + " you've caught a "
                + str(pokemon_name.capitalize())
                + "! "
                + link
                + " Gotta catch 'em all!"
            )
        except beckett.exceptions.InvalidStatusCodeError as e:
            print(e)
            await ctx.channel.send(str(await botDB.getEscapePhrase()))

    @commands.command(name="pokedex")
    async def pokedex(self, ctx, *, msg=None) -> None:
        if msg == "reset":
            await ctx.channel.send("Are you sure? (y/n)")
            response = await self.bot.wait_for(
                "message",
                predicate=lambda m: m.author.name != self.bot.nick
                and m.author == ctx.author,
            )
            if response[0].content == "y" or response[0].content == "yes":
                await botDB.remove_all_pokemon(int(ctx.author.id))
                await ctx.channel.send("Pokedex reset!")
            else:
                await ctx.channel.send("Pokedex not reset.")
            return

        if msg == "release":
            await self.release(ctx)
            return

        if msg == "deviation":
            mons = await botDB.getPokedex(ctx.author.name)
            spread = {}
            total = 0
            check = 0
            for mon in mons:
                first_letter = mon["pokemon_name"][0]
                try:
                    spread[f"{first_letter}"] += 1
                    continue
                except KeyError:
                    spread[f"{first_letter}"] = 0
                spread[f"{first_letter}"] += 1
            for key in spread:
                total += spread[f"{key}"]
            for key in spread:
                spread[f"{key}"] = str(round((spread[f"{key}"] / total) * 100, 2)) + "%"
            await ctx.channel.send(spread)
            return

        if "count" in str(msg).split(" "):
            print("count")
            msg = msg.split(" ")
            if len(msg) > 2:
                await ctx.channel.send(
                    "Invalid command, please provide a single user, or no user to see your own."
                )
                return
            if len(msg) == 1:
                user = ctx.author.name
            else:
                msg.remove("count")
                user = msg[0]
            mons = await botDB.getPokedex(user)
            await ctx.channel.send(f"{user}'s pokemon count is: " + str(len(mons)))
            return

        pokemons = ""
        if msg is None:
            msg = ctx.author.name
        mons = await botDB.getPokedex(msg.lower())
        if len(mons) == 0:
            await ctx.channel.send("No pokemon found, use !mon to catch one!")
            return
        for mon in mons:
            if len(pokemons + mon["pokemon_name"] + ", ") < 500:
                pokemons += mon["pokemon_name"] + ", "
            if len(pokemons + mon["pokemon_name"] + ", ") > 500:
                await ctx.channel.send(pokemons)
                pokemons = ""
                await sleep(1)
        print("end")
        await ctx.channel.send(pokemons)

    async def release(self, ctx: commands.Context):
        await ctx.channel.send("Who do you wish to release?")
        response = await self.bot.wait_for(
            "message", predicate=lambda m: m.author == ctx.author, timeout=60
        )
        print(response[0].content)

    # TODO: check if user has pokemon
    # TODO: check only for plausible answers
    # command to trade pokemon between 2 users
    @commands.command(name="trade", aliases=["t"])
    async def trade(self, ctx: commands.Context, *, msg=None):
        name1 = ctx.author.name
        id1 = ctx.author.id
        await ctx.channel.send("Who do you wish to trade with?")
        name2 = await self.bot.wait_for(
            "message",
            predicate=lambda m: ctx.author.name != self.bot.nick
            and m.author == ctx.author,
            timeout=60,
        )
        name2 = name2[0].content
        await ctx.channel.send(f"@{name2}, would u like to trade with {name1}?")
        answer = await self.bot.wait_for(
            "message",
            predicate=lambda m: ctx.author.name != self.bot.nick
            and m.author.name == name2,
        )
        id2 = answer[0].author.id
        if answer[0].content == "no":
            await ctx.channel.send(f"{name2} did not agree to trade. Trade cancelled")
            return
        await ctx.channel.send(f"@{name1}, which pokemon would you like to trade?")
        mon1 = await self.bot.wait_for(
            "message",
            predicate=lambda m: ctx.author.name != self.bot.nick
            and m.author.name == name1,
            timeout=60,
        )
        mon1 = mon1[0].content
        await ctx.channel.send(f"@{name2}, which pokemon would you like to trade?")
        mon2 = await self.bot.wait_for(
            "message",
            predicate=lambda m: ctx.author.name != self.bot.nick
            and m.author.name == name2,
            timeout=60,
        )
        mon2 = mon2[0].content
        names = [name1, name2]
        await ctx.channel.send(
            f"Do you both agree to trade {name1}'s {mon1} for {name2}'s {mon2}? (yes/no)"
        )
        for name in names[:]:
            agreement = await self.bot.wait_for(
                "message",
                predicate=lambda m: ctx.author.name != self.bot.nick
                and m.author.name in names,
                timeout=60,
            )
            if agreement[0].content in ("yes", "y"):
                names.remove(agreement[0].author.name)
        if names:
            await ctx.channel.send(
                "One of you did not agree, or prompt timed out (30s), trade cancelled"
            )
            return
        id1 = int(id1)
        id2 = int(id2)
        if await botDB.exchange_pokemon(
            user_id=id1,
            pokemon_name=mon1,
            user_id2=id2,
            pokemon_name2=mon2,
            username=name1,
            username2=name2,
        ):
            await ctx.channel.send("Trade successful!")
            return
        else:
            await ctx.channel.send("Trade failed!")
            return


def prepare(bot: commands.Bot):
    # Load our cog with this module...
    bot.add_cog(pokedex_cog(bot))
