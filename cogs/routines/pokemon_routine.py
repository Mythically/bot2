import asyncio
import time
from random import randint

from twitchio.ext import routines
from twitchio.ext import commands


class pokemon_routine(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # send message to all channels the bot currently is in
    # TODO: extract get pokemon, and add pokemon to db methods
    # TODO: get mon in pre-routine hook, send message, in post-book update db
    # TODO: send result message only in channels where people participated
    @routines.routine(hours=2)
    async def broadcast(self, ctx: commands.Context) -> None:
        users = []
        pokemon_id = randint(0, 1126)
        pokemon = self.pokemonClient.get_pokemon(pokemon_id)
        pokemon_name = pokemon.forms[0].name
        for chan in self.connected_channels:
            await chan.send(
                f'A wild {pokemon_name} has appeared! Type "catch" for a chance to catch it! You have 20 seconds.'
            )
        try:
            countdown = time.time()
            print(countdown - time.time())
            while (countdown - time.time()) < 20:
                user = await self.wait_for(
                    "message", lambda m: not m.echo and m.content == "catch", timeout=20
                )
                print(user[0].author.name)
                print(user[0].content)
                users += user
        except asyncio.TimeoutError:
            print("Timeout")
            chosen = randint(0, len(users))
            await ctx.channel.send(
                f"{len(users)} trainers tried to catch the pokemon, @{users[chosen].author.name} caught it!"
                " It will be sent to your pokedex, good job!"
            )
