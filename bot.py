#!/usr/bin/env python3
import asyncio
import beckett.exceptions
import botDB
import datetime
import emoji
import math
import os
import pokepy
import re
import requests
import signal
import subprocess as sp
from asyncio import sleep
from random import randint

import openai
# from spellchecker import SpellChecker
# from twitchio import Channel, User, Client
from twitchio.ext import commands

import spotify_playing


# from tqdm import tqdm

# some vars


# client_disk_cache = pokepy.V2Client(cache='in_disk', cache_location='/temp')


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ["TMI_TOKEN"],
            client_id=os.environ["CLIENT_ID"],
            nick=os.environ["BOT_NICK"],
            prefix=os.environ["BOT_PREFIX"],
            initial_channels=os.environ["CHANNELS"].split(","),
        )

    i = 0
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pokemonClient = pokepy.V2Client()
    trusted_users = []

    # bot.py, below bot object
    async def event_ready(self) -> None:
        print(f"Logged into {bot.connected_channels} | {bot.nick}")
        self.trusted_users = await botDB.get_trusted_users()
        print(self.trusted_users)

    async def event_message(self, msg) -> None:
        if msg.echo:
            return
        if "gift me" in msg.content.lower():
            await msg.channel.send(f"/timeout {msg.author.name} 1m ")
        if "hello" in msg.content.lower():
            if msg.channel.name == "themythh":
                print("no")
                return
            await msg.channel.send(f"Hi, @{msg.author.name}!")
        if msg.content:
            self.i += 1

            if "messages" in msg.content.lower():
                if msg.author.name == "themythh":
                    await msg.channel.send(str(self.i))
        # if " what " and " song " in a.content.lower():
        #     spotify_playing.get_current_track()

        # print(get_user(a.author.name))

        # await msg.channel.send(msg.content)
        # await msg.channel.send(msg.author.name)

        # @bot.event()
        # async def event_message(a):
        #     global words
        #     check = a.raw_data.split(':')[2]
        #     check = check.split()
        #     check = spell_check(check)
        #     if a.echo:
        #         words = ''
        #         return
        #     if "!reason" in check:
        #         return
        #     if check:
        #         await a.channel.send("pepePoint " + check)
        #     words = ''
        #

        if self.is_trusted_user(msg.author.name) or msg.author.is_mod or msg.author.is_subscriber or \
                msg.author.is_broadcaster:
            regex = (
                r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()"
                r"<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            )
            if re.search(regex, msg.content):
                await msg.channel.send("/timeout " + msg.author.name + " 1m")
                await msg.channel.send(
                    f"[WARNING] @{msg.author.name} If you are not subscribed, please ask a moderator to send your link."
                )
        if msg.author:
            author = str(msg.author).split()
            words2 = msg.content.split()
            name = msg.author.name.lower()
            if msg.echo:
                return
            user_id = int(msg.author.id)
            # await botDB.updateMessages(name, user_id)
            # if "nightbot" in word:
            # if "caught" in words2:
            #     pokemon_name = words2[4].strip("!")
            #     pokemon = [pokemonClient.get_pokemon(pokemon_name.lower())]
            #     pokemon_id = pokemon[0].id
            #     await msg.channel.send(
            #         f"Detected pokemon: {pokemon_name}, #{pokemon_id}"
            #     )
            for word in author:
                if "stream" in word:
                    for word in words2:
                        if "hoss" in word and word != "frathoss":
                            await msg.channel.send(f"/ban {word}")
                            await msg.channel.send(
                                "Another hoss bites the dust PogChamp"
                            )
            if (
                    "buy" in msg.content
                    and "followers" in msg.content
                    and "viewers" in msg.content
                    and "primes" in msg.content
            ):
                await msg.channel.send(f"/ban {name}")
        await self.handle_commands(msg)

    # @commands.command(name="user")
    # async def users(msg):
    #     response = requests.get("https://api.twitch.tv/helix/users?login=zack_ko")
    #     fetch = response.json()
    #     print(fetch)
    #
    #
    # @client.event()
    # async def event_raw_usernotice(channel: Channel, tags: dict):
    #     print("Channel " + str(channel) + " tags " + str(tags))
    #     listing = tags.items()
    #     stringify = ""
    #     for item in range(len(listing)):
    #         stringify += item
    #
    #     print("TAGS: " + stringify)
    #     if "first-msg" in tags:
    #         await channel.send("First message")
    #

    # @client.event()
    # async def event_pubsub_bits(event):
    #     print("bits redemption" + str(event))
    #     chan = client.get_channel(current_channel)
    #     await chan.send("Cheer!")

    # @commands.command(name="reason")
    # async def reason(ctx, *, msg):
    #     await ctx.channel.send(spell_correction(msg))
    #

    @commands.command(name="test")
    async def test(self, msg) -> None:
        print("test")
        await msg.channel.send("test passed!")

    @commands.command(name="type")
    async def types2(self, ctx, *, msg) -> None:
        pokemon = [pokepy.V2Client().get_pokemon(msg.lower())]
        pokemon_type = ""
        for x in range(len(pokemon[0].types)):
            pokemon_type += pokemon[0].types[x].type.name
            pokemon_type += " "
        await ctx.channel.send(str(pokemon_type))
        # return list(pokemon_type)

    @commands.command(name="weak")
    async def ww(self, ctx, *, msg) -> None:
        if " " in msg:
            msg = msg.replace(" ", "-")
        typings = ""
        damage = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}
        pokemon = [self.pokemonClient.get_pokemon(msg.lower())]
        # print(pokemon)
        if pokemon:
            pokemon_type = []
            for x in range(len(pokemon[0].types)):
                pokemon_type.append(pokemon[0].types[x].type.name)
            for j in range(len(pokemon_type)):
                # print(pokemon_type[j])
                typings += pokemon_type[j]
                typings += " "
                # print(typings)

            if len(pokemon_type) != 0:
                pass
                # await ctx.channel.send(pokemon[0].name + ' is: ' + str(pokemon_type) + ' and is weak to: ')
            else:
                pokemon_type = msg.split()
                # print(str(pokemon_type))
        x = 1
        loop = 0
        if pokemon_type:
            for typing in pokemon_type:

                g = 0
                # print('loop')
                response = requests.get(f"https://pokeapi.co/api/v2/type/{typing}")
                fetch = response.json()
                # print(typing)
                for effect, types in fetch["damage_relations"].items():
                    if x % 2 != 0:
                        if loop == 0:
                            g += 1
                        test2 = [type["name"] for type in types]
                        # print(test2)
                        if g == 1:
                            for fetch_weak in test2:
                                damage["2x"].append(fetch_weak)

                        if g == 2:
                            for fetch_weak in test2:
                                damage["0.5x"].append(fetch_weak)

                        if g == 3:
                            for fetch_weak in test2:
                                damage["0x"].append(fetch_weak)

                        if loop == 1:
                            g += 1
                            if g == 1:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["4x"].append(fetch_weak)
                                    if fetch_weak not in damage["2x"]:
                                        damage["2x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        damage["2x"].remove(fetch_weak)
                                    if fetch_weak in damage["0.5x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["1x"].append(fetch_weak)

                            if g == 2:
                                for fetch_weak in test2:
                                    print(fetch_weak)
                                    if fetch_weak not in damage["0.5x"]:
                                        damage["0.5x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["0.5x"]:
                                            damage["0.5x"].remove(fetch_weak)
                                    if fetch_weak in damage["2x"]:
                                        print(fetch_weak + "in 2x")
                                        damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)

                                        print(damage["2x"])

                            if g == 3:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["4x"]:
                                        damage["4x"].remove(fetch_weak)
                                    elif fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)

                    x += 1
                loop += 1

        for type in damage["0x"]:
            for type in damage["0x"]:
                if type in damage["2x"]:
                    damage["2x"].remove(type)
            if type in damage["4x"]:
                damage["4x"].remove(type)
        for type in damage["2x"]:
            if type in damage["4x"]:
                damage["2x"].remove(type)

        message1 = ""
        message2 = ""
        if damage["4x"]:
            message1 = ", ".join(damage["4x"])
            # for x in range(len(damage['4x'])):
            #     message += damage['4x'][x]
        if damage["2x"]:
            message2 = ", ".join(damage["2x"])

        if message1:
            await ctx.channel.send(
                pokemon[0].name
                + " is: "
                + typings
                + " takes 4x: "
                + message1
                + "; 2x: "
                + message2
            )
            return
        await ctx.channel.send(
            pokemon[0].name + " is: " + typings + " takes 2x: " + message2
        )

    @commands.command(name="w")
    async def weak_type(self, ctx, *, msg) -> None:
        damage = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}
        pokemon_type = msg.split()
        x = 1
        loop = 0
        if pokemon_type:
            for typing in pokemon_type:

                g = 0
                # print('loop')
                response = requests.get(f"https://pokeapi.co/api/v2/type/{typing}")
                fetch = response.json()
                # print(typing)
                for effect, types in fetch["damage_relations"].items():
                    if x % 2 != 0:
                        if loop == 0:
                            g += 1
                        test2 = [type["name"] for type in types]
                        # print(test2)
                        if g == 1:
                            for fetch_weak in test2:
                                damage["2x"].append(fetch_weak)

                        if g == 2:
                            for fetch_weak in test2:
                                damage["0.5x"].append(fetch_weak)

                        if g == 3:
                            for fetch_weak in test2:
                                damage["0x"].append(fetch_weak)

                        if loop == 1:
                            g += 1
                            if g == 1:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["4x"].append(fetch_weak)
                                    if fetch_weak not in damage["2x"]:
                                        damage["2x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        damage["2x"].remove(fetch_weak)
                                    if fetch_weak in damage["0.5x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["1x"].append(fetch_weak)

                            if g == 2:
                                for fetch_weak in test2:
                                    print(fetch_weak)
                                    if fetch_weak not in damage["0.5x"]:
                                        damage["0.5x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["0.5x"]:
                                            damage["0.5x"].remove(fetch_weak)
                                    if fetch_weak in damage["2x"]:
                                        print(fetch_weak + "in 2x")
                                        damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)

                                        print(damage["2x"])

                            if g == 3:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["4x"]:
                                        damage["4x"].remove(fetch_weak)
                                    elif fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)

                    x += 1
                loop += 1

        for type in damage["0x"]:
            for type in damage["0x"]:
                if type in damage["2x"]:
                    damage["2x"].remove(type)
            if type in damage["4x"]:
                damage["4x"].remove(type)
        for type in damage["2x"]:
            if type in damage["4x"]:
                damage["2x"].remove(type)

        message = ""
        if damage["4x"]:
            message += "4x: " + str(damage["4x"])
            # for x in range(len(damage['4x'])):
            #     message += damage['4x'][x]
        if damage["2x"]:
            message += " 2x: " + str(damage["2x"])

        await ctx.channel.send(str(message))

    @commands.command(name="trigger")
    async def trigger(self, ctx, *, msg) -> None:
        if msg.isnumeric() is True:
            pokemon_id = msg
        elif msg.isnumeric() is False:
            pokemon = [self.pokemonClient.get_pokemon(msg.lower())]
            pokemon_id = pokemon[0].id
            print(pokemon, pokemon_id)
        pokemon = [self.pokemonClient.get_pokemon(msg.lower())]
        # print(pokemon_id)
        id = [self.pokemonClient.get_pokemon_species(pokemon_id)]
        pokemon_species_id = id[0].evolution_chain.url
        pokemon_evolution_id = pokemon_species_id.split("/")[-2]
        print(pokemon_evolution_id)
        pokemon_evolution = [self.pokemonClient.get_evolution_chain(pokemon_evolution_id)]
        # print(str(pokemon_species_id) + " chain")
        # print(pokemon_evolution_id)
        # pokemon_trigger = pokemon_evolution[0].chain.evolves_to[0].evolution_details[0].trigger.name
        # print(pokemon_trigger)
        # pokemon_evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolution_details
        pokemon_name1 = pokemon_evolution[0].chain.species.name
        pokemon_name2 = pokemon_evolution[0].chain.evolves_to[0].species.name
        try:
            pokemon_name3 = (
                pokemon_evolution[0].chain.evolves_to[0].evolves_to[0].species.name
            )
        except IndexError:
            pokemon_name3 = None
        # print(msg)
        # print(pokemon[0].name)
        # print(pokemon_name1 + "1st evolution")
        # print(pokemon_name2 + "2nd evolution")
        pokemon_message = " "
        names = ""
        if pokemon[0].name == pokemon_name1:
            evolution_details = (
                pokemon_evolution[0].chain.evolves_to[0].evolution_details[0]
            )
            names += pokemon[0].name + " -> " + pokemon_name2 + "; "
        elif pokemon[0].name == pokemon_name2:
            evolution_details = (
                pokemon_evolution[0]
                .chain.evolves_to[0]
                .evolves_to[0]
                .evolution_details[0]
            )
            names += pokemon[0].name + " -> " + pokemon_name3 + "; "
        elif pokemon[0].name == pokemon_name3:
            await ctx.channel.send(f"{pokemon[0].name} doesn't evolve AFAIK :3")
        else:
            evolution_details = (
                pokemon_evolution[0]
                .chain.evolves_to[0]
                .evolves_to[0]
                .evolution_details[0]
            )
        trigger_level = evolution_details.min_level
        trigger_affection = evolution_details.min_affection
        trigger_time = evolution_details.time_of_day
        trigger_trade = evolution_details.trade_species
        trigger_move = evolution_details.known_move
        trigger_move_type = evolution_details.known_move_type
        trigger_item = evolution_details.item
        trigger_held_item = evolution_details.held_item
        trigger_happiness = evolution_details.min_happiness

        if trigger_happiness is not None:
            pokemon_message += "Min happiness: " + str(trigger_happiness)
        if trigger_level is not None:
            pokemon_message += "Min level: " + str(trigger_level)
        if trigger_affection is not None:
            pokemon_message += "Min affection: " + str(trigger_affection)
        if trigger_time != "":
            pokemon_message += "Time of the day: " + str(trigger_time)
        if trigger_trade is not None:
            pokemon_message += "Needs to be traded!"
        if trigger_move is not None:
            pokemon_message += "Needs to know a move:   " + str(trigger_move).replace(
                "<Named_API_Resource |", ""
            ).replace(">", "")
        if trigger_move_type is not None:
            pokemon_message += "Needs to know a move of type: " + str(trigger_move_type)
        if trigger_item is not None:
            pokemon_message += "Needs an item to evolve: " + str(trigger_item.name)
        if trigger_held_item is not None:
            pokemon_message += "Needs to hold item to evolve: " + str(trigger_held_item)

        if pokemon_message == " ":
            await ctx.channel.send(
                "Another evolution trigger that I have not accounted for yet, please bare with me :3"
            )
            return
        await ctx.channel.send(names + ": " + pokemon_message)

    @commands.command(name="move")
    async def move(self, ctx, *, msg) -> None:
        # ctx.channel.send(msg)
        if " " in msg:
            msg = msg.replace(" ", "-")
        # print(msg)
        move = [self.pokemonClient.get_move(msg)]
        type = str(move[0].type.name)
        damage_class = str(move[0].damage_class.name)
        power = str(move[0].power)
        pp = str(move[0].pp)
        priority = str(move[0].priority)
        accuracy = str(move[0].accuracy)
        effect_chance = str(move[0].effect_chance)
        effect_entries = str(move[0].effect_entries[0].effect).replace(
            " $effect_chance", " " + effect_chance
        )
        if (
                len(
                    type.capitalize()
                    + "; "
                    + damage_class.capitalize()
                    + " Power: "
                    + power
                    + " Accuracy: "
                    + accuracy
                    + " PP: "
                    + pp
                    + " Priority: "
                    + priority
                    + "  "
                    + effect_entries
                )
                >= 500
        ):
            await ctx.channel.send(
                type.capitalize()
                + "; "
                + damage_class.capitalize()
                + " Power: "
                + power
                + " PP: "
                + pp
                + " Priority: "
                + priority
                + "  "
            )
            if len(effect_entries) > 500:
                split_entries = effect_entries.split(".")
                len_split_entries = len(split_entries)
                first_half = ""
                second_half = ""
                for index in range(len_split_entries):
                    if index < len_split_entries // 2:
                        first_half += split_entries[index] + "."
                    else:
                        second_half += split_entries[index] + "."
                await ctx.channel.send(first_half)
                await ctx.channel.send(second_half)
                return
            await ctx.channel.send(effect_entries)
            return
        await ctx.channel.send(
            type.capitalize()
            + "; "
            + damage_class.capitalize()
            + " Power: "
            + power
            + " PP: "
            + pp
            + " Priority: "
            + priority
            + "  "
            + effect_entries
        )

    @commands.command(name="vanish")
    async def time_outed(self, msg) -> None:
        if msg.author.name != bot.nick:
            print(f"/timeout {msg.author.name}")
            await msg.channel.send(f"/timeout {msg.author.name} 1s")

    # @commands.command(name='resets')
    # async def resets(msg):
    #     await msg.channel.send('0 resets baby, THIS IS THE RUN LETSGO !!!!')

    @commands.command(name="kill")
    async def kill(self, msg) -> None:
        print(msg.channel.name)

        if (
                msg.author.is_broadcaster
                or msg.author.name == "themythh"
                or msg.author.is_mod
        ):
            await msg.channel.send("Bye! :)")
            await bot.close()

    @commands.command(name="timer")
    async def timer(self, ctx, *, msg) -> None:
        if "s" in msg:
            msg = msg[:-1]
        if "m" in msg:
            msg = msg[:-1]
            msg = int(msg)
            msg *= 60
        if int(msg) > 0:
            mins = int(msg) / 60
            secs = str(int(msg) % 60) + "s"
            hours = mins / 60
            hours = str(math.floor(hours)) + "h"
            mins = mins % 60
            mins = str(round(mins)) + "m"
            if mins == "0m":
                mins = ""
            if hours == "0h":
                hours = ""
            if secs == "0s":
                secs = ""
            await ctx.channel.send("Timer " + hours + mins + secs + " started :)")
            await sleep(int(msg))
            await ctx.channel.send(
                "Timer of " + hours + mins + secs + ", just ran out!"
            )

    @commands.command(name="ryan")
    async def ryan(self, msg) -> None:
        await msg.channel.send("FeelsAmazingMan oiler")

    @commands.command(name="lag")
    async def lag(self, msg) -> None:
        if msg.author.name == "themythh":
            while True:
                await sleep(1)
                await msg.channel.send("SourPls LAG THE CHAT SourPls ")

    @commands.command(name="so")
    async def so(self, ctx, *, msg) -> None:
        game = await self.fetch_channel(msg)
        await ctx.channel.send(
            "Yo what are you waiting for, go check out "
            + msg
            + " at www.twitch.tv/"
            + msg +
            "they were last playing"
            + game
        )

    @commands.command(name="dance")
    async def dance(self, msg) -> None:
        if msg.author.name == "themythh":
            while True:
                await sleep(5)
                await msg.channel.send("SourPls")

    @commands.command(name="brain")
    async def dance(self, msg) -> None:
        if msg.author.name == "themythh":
            while True:
                await sleep(1)
                await msg.channel.send(
                    "/me O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee "
                    "AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA "
                )

    @commands.command(name="coinflip", aliases=["cf"])
    async def coinflip(self, msg) -> None:
        number = randint(1, 2)
        if number == 1:
            await msg.channel.send("It landed on HEADS")
        else:
            await msg.channel.send("It landed on TAILS")

    @commands.command(name="killskygod")
    async def killskygod(self, msg) -> None:
        await msg.channel.send("/ban RollingSkyGod")

    @commands.command(name="saveskygod")
    async def saveskygod(self, msg) -> None:
        await msg.channel.send("/unban RollingSkyGod")

    # @commands.command(name="reset", aliases=["t"])
    # async def reset(ctx, *, msg):
    #     if reset in msg:
    #         await bot.close()
    #         await bot.join_channels([ctx.channel.name])

    # @commands.command(name='brain')
    # async def brian(msg):
    #     while True:
    #         await sleep(0.5)
    #         await msg.channel.send('/me  O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA ')

    @commands.command(name="join")
    async def join(self, ctx, *, msg) -> None:
        channel_name = [msg]
        await bot.join_channels(channel_name)
        await ctx.channel.send("Joined channel: " + str(channel_name))
        print(channel_name)

    # leave current channel
    @commands.command(name="leave", aliases=["l"])
    async def leave(self, ctx: commands.Context):
        await ctx.channel.send("Leaving channel, bye!")
        await self.part_channels([ctx.channel.name])

    @commands.command(name="mon")
    @commands.cooldown(rate=2, per=30, bucket=commands.Bucket.user)
    async def pokemon(self, ctx) -> None:
        try:
            pokemon_id = randint(0, 1126)
            if pokemon_id > 903:
                await ctx.channel.send(await botDB.getEscapePhrase())
                return
            pokemon = self.pokemonClient.get_pokemon(pokemon_id)
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
            response = (await self.wait_for('message', predicate=lambda m: m.author == ctx.author))
            print(response)
            if response.content == "y" or response.content == "yes":
                await botDB.resetPokedex(ctx.author.id)
                await ctx.channel.send("Pokedex reset!")
            else:
                await ctx.channel.send("Pokedex not reset.")
            return
        elif msg == "release":
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

        await ctx.channel.send(pokemons)

    @commands.command(name="ban")
    async def ban(self, msg) -> None:
        for x in range(1, 10000):
            await sleep(0.3)
            await msg.channel.send(f"/ban hoss{x}")
            await sleep(0.3)
            await msg.channel.send(f"/ban hossoo_{x}")
            await sleep(0.3)
            await msg.channel.send(f"/ban hoss00{x}")
            await sleep(0.3)
            await msg.channel.send(f"/ban hoss000{x}")
            await sleep(0.3)
            await msg.channel.send(f"/ban h0ssoo{x}")
            await sleep(0.3)
            await msg.channel.send(f"/ban h0ss__{x}")
            await sleep(0.3)
            await msg.channel.send(f"/ban hoss__{x}")
            await sleep(0.3)
            await msg.channel.send(f"/ban hoss00{x}__")
            await sleep(0.3)

    @commands.command(name="ban2")
    async def banTXT(self, ctx) -> None:
        file = open("ban.txt", "r")
        # count = 0
        for line in file:
            # count += 1
            # if count > 600:
            await sleep(2)
            await ctx.channel.send(f"{line.strip()}")
        file.close()

    # @commands.command()
    # async def change_dict(ctx, *, msg):
    #     global spell
    #     if "english" in msg.lower():
    #         spell = SpellChecker(language='en')
    #     if "spanish" in msg.lower():
    #         spell = SpellChecker(language='es')
    #     if "french" in msg.lower():
    #         spell = SpellChecker(language='fr')
    #     if "portuguese" in msg.lower():
    #         spell = SpellChecker(language='pt')
    #     if "german" in msg.lower():
    #         spell = SpellChecker(language='de')
    #     if "russian" in msg.lower():
    #         spell = SpellChecker(language='ru')
    #
    #     await ctx.channel.send("Dictionary set to "+msg)

    # @commands.command(name="leave")
    # async def leave(ctx, *, msg):
    #     channel_name = [msg]
    #     await bot.

    @commands.command()
    async def bttvemotes(self, ctx, *, msg=None) -> None:
        if msg is None:
            print(msg, ctx.channel.name)
            msg = ctx.channel.name
        emotesString = ""
        counter = 0
        response = requests.get("https://decapi.me/bttv/emotes/" + msg)
        fetch = response.text
        fetch = fetch.split(" ")
        for numbers, word in enumerate(fetch):
            if len(emotesString + word) < 500:
                emotesString += word + " "
                counter += 1
            if (len(emotesString + word) > 500) or (numbers == len(fetch) - 1):
                await ctx.channel.send(emotesString)
                emotesString = ""
                counter = 0
                await sleep(2)

    @commands.command(name="7tvemotes")
    async def seventvemotes(self, ctx, *, msg=None) -> None:
        if msg is None:
            print(msg, ctx.channel.name)
            msg = ctx.channel.name
        emotesString = ""
        counter = 0
        response = requests.get(f"https://api.7tv.app/v2/users/{msg}/emotes")
        fetch = response.json()
        for numbers, word in enumerate(fetch):
            # print(word['name'])
            if len(emotesString + word["name"]) < 500:
                emotesString += word["name"] + " "
                counter += 1
            if (len(emotesString + word["name"]) > 500) or (numbers == len(fetch) - 1):
                await ctx.channel.send(emotesString)
                emotesString = ""
                counter = 0
                await sleep(2)

    @commands.command()
    async def ffzemotes(self, ctx, *, msg=None) -> None:
        emoteString = ""
        if msg is None:
            print(msg, ctx.channel.name)
            msg = ctx.channel.name

        response = requests.get("https://api.frankerfacez.com/v1/room/" + msg)
        fetch = response.json()
        for account, id in fetch["sets"].items():
            for emoticon in id["emoticons"]:
                emoteString += str(emoticon["name"] + " ")
        await ctx.channel.send(emoteString)

    def ffzemotes2(self, msg) -> str:
        emoteString = ""
        response = requests.get("https://api.frankerfacez.com/v1/room/" + msg)
        fetch = response.json()

        for account, id in fetch["sets"].items():
            for emoticon in id["emoticons"]:
                emoteString += str(emoticon["name"] + " ")
        return emoteString

    @commands.command(name="song")
    async def spotify_current_song(self, ctx) -> None:
        if botDB.checkIfAlreadyInserted(ctx.channel.name):
            current_song = spotify_playing.get_song(ctx.channel.name, ctx.channel)
            await ctx.channel.send(current_song)
        else:
            await ctx.channel.send(
                "It seems that this channel has not yet linked their spotify, please check with the "
                "broadcaster."
            )

    @commands.command(name="spotify")
    async def spotify_token(self, ctx) -> None:
        await ctx.channel.send(
            "You can sign up here :) -> https://accounts.spotify.com/authorize?client_id"
            "=90082084b6b6423f8f08dd85e74f42b4&response_type=code&redirect_uri=https://b816-103-219-21"
            "-123.eu.ngrok.io/&scope=user-read-currently-playing"
        )

    @commands.command(name="checkKey")
    async def checkSpotifyToken(self, ctx) -> None:
        await ctx.channel.send(botDB.checkSpotifyRefreshToken(ctx.author.name))

    async def send_message(self, msg, channel):
        await channel.send(msg)

    @commands.command(name="sayfile")
    async def sayfile(self, ctx, *, msg) -> None:
        response = requests.get(f"{msg}")
        bans = response.text.split("\n")
        print(bans, type(bans))
        for line in bans:
            await ctx.channel.send(str(line))
            await sleep(0.3)

    @commands.command()
    async def pyramid(self, ctx, *, msg) -> None:
        new = msg.split(" ")
        limit = 5
        if ctx.author.is_broadcaster:
            limit = 48
        if not str(new[1]).isnumeric():
            await ctx.channel.send(
                f'Does "{new[1]}" look like a number to you!? Madge '
            )
            return
        x = int(new[1])

        if x > limit and ctx.author.name == "ws_zoomers":
            await ctx.channel.send(f"{limit} is the limit, you are asking for {x}")
            await ctx.channel.send("I know it's fun, but chill out")
            return
        column = ""

        for rows in range(x):
            await asyncio.sleep(1)
            column += new[0] + " "
            if len(column) > 500:
                await ctx.channel.send("Message is longer than 500 characters")
                return
            await ctx.channel.send(column)
        column = column.rsplit(" ", 1)[0]

        for row in range(x - 1, 0, -1):
            await asyncio.sleep(1)
            column = column.rsplit(" ", 1)[0]
            await ctx.channel.send(column)

    @commands.command(name="r")
    async def randd(self, ctx, *, msg="None") -> None:
        number = randint(1, 3)
        await ctx.channel.send(str(number))

    @commands.command()
    async def dia(self, ctx, *, msg=None) -> None:
        if msg is None:
            await ctx.channel.send("Please send a message")
        # response = (await bot.wait_for('message', predicate=lambda m: m.author == ctx.author))
        await ctx.channel.send(msg)

    @commands.command()
    async def fog(self, ctx) -> None:
        await ctx.channel.send(emoji.emojize(":fog:"))

    @commands.command(name="fact")
    async def facts(self, ctx, *, msg=None) -> None:
        if msg is None:
            facts = ["random/math", "random/trivia"]
            number = randint(0, 1)
            await ctx.channel.send(
                requests.get("http://numbersapi.com/" + facts[number]).text
            )

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, msg=None) -> None:
        if msg is None:
            await ctx.channel.send("Please ask a question")
            return
        answers = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
        ]
        await ctx.channel.send(answers[randint(0, len(answers) - 1)])

    # use pokeapi.com to get pokemon info
    # messages should be less than 500 characters
    # @commands.command()
    # async def pokemon2(self, ctx, *, msg=None):
    #     if msg is None:
    #         await ctx.channel.send("Please enter a pokemon name")
    #         return
    #     response = requests.get("https://pokeapi.co/api/v2/pokemon/" + msg)
    #     if response.status_code == 404:
    #         await ctx.channel.send("Pokemon not found")
    #         return
    #     response = response.json()
    #     await ctx.channel.send(
    #         f"{response['name']} is a {response['height']} tall {response['weight']} heavy {response['types'][0]['type']['name']}"
    #     )
    #     await ctx.channel.send(f"{response['abilities'][0]['ability']['name']}")
    #     await ctx.channel.send(f"{response['stats'][5]['base_stat']}")
    #     await ctx.channel.send(f"{response['stats'][4]['base_stat']}")
    #     await ctx.channel.send(f"{response['stats'][3]['base_stat']}")
    #     await ctx.channel.send(f"{response['stats'][2]['base_stat']}")
    #     await ctx.channel.send(f"{response['stats'][1]['base_stat']}")
    #     await ctx.channel.send(f"{response['stats'][0]['base_stat']}")
    #     await ctx.channel.send(f"{response['sprites']['front_default']}")
    #     await ctx.channel.send(f"{response['sprites']['front_shiny']}")
    #     await ctx.channel.send(f"{response['sprites']['back_default']}")
    #     await ctx.channel.send(f"{response['sprites']['back_shiny']}")

    # use pokepy to decide what types are strong against each other in one message
    # message length should be less than 500 characters
    # verify if list index is out of range
    # @commands.command(name="types")
    # async def types(self, ctx, *, msg=None):
    #     if msg is None:
    #         await ctx.channel.send("Please enter a type")
    #         return
    #     response = requests.get("https://pokeapi.co/api/v2/type/" + msg)
    #     if response.status_code == 404:
    #         await ctx.channel.send("Type not found")
    #         return
    #     response = response.json()
    #     await ctx.channel.send(
    #         f"{response['name']} is weak to: {response['damage_relations']['double_damage_from'][0]['name']}"
    #     )
    #     await ctx.channel.send (
    #         f"{response['name']} is strong against: {response['damage_relations']['double_damage_to'][0]['name']}"
    #     )
    #     await ctx.channel.send(
    #         f"{response['name']} is immune to: {response['damage_relations']['no_damage_from'][0]['name']}"
    #     )
    #     await ctx.channel.send(
    #         f"{response['name']} is weak to: {response['damage_relations']['half_damage_from'][0]['name']}"
    #     )
    #     await ctx.channel.send(
    #         f"{response['name']} is resistant against: {response['damage_relations']['half_damage_to'][0]['name']}"
    #     )
    #     await ctx.channel.send(
    #         f"{response['name']} is deals no damage to: {response['damage_relations']['no_damage_to'][0]['name']}"
    #     )

    # return long and lat of a city using openweathermap direct geocoding
    # save city name and long and lat to sql database
    def get_city_coords(self, city_name) -> [int]:
        print(city_name)
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q="
            + city_name
            + "&appid="
            + os.environ["OPENWEATHERMAP_API_KEY"]
        )
        if response.status_code == 404:
            return "Could not find city"
        response = response.json()
        return response["coord"]["lat"], response["coord"]["lon"]

    # use coords_city() to get the weather of a city from openweathermap 2.5 api
    @commands.command(name="weather")
    async def weather(self, ctx: commands.Context, *, msg=None) -> None:
        coords = []
        if msg is None:
            if await botDB.is_location_set(int(ctx.author.id)):
                coords = await botDB.get_location(int(ctx.author.id))
                lat = coords[0]['lat']
                lon = coords[0]['lon']
            else:
                await ctx.channel.send("Please enter a city, or set your location with !set_location")
                return
        # check if list is empty
        if not coords:
            coords = self.get_city_coords(msg)
            if coords == "Could not find city":
                await ctx.channel.send("Couldn't get city coordinates. Please check spelling and try again.")
                return
            lat = coords[0]
            lon = coords[1]
            print(lat)
            print(lon)
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid="
            f"{os.environ['OPENWEATHERMAP_API_KEY']}&units=metric")
        if response.status_code == 404:
            await ctx.channel.send("City not found")
            return

        response = response.json()
        emoji_icon = self.emoji_choice(response['weather'][0]['description'])
        wind_direction = self.deg_to_cardinal(response['wind']['deg'])
        # convert sunrise and sunset to city's timezone
        try:
            weather = f"{ctx.author.name}, {response['name']},{response['sys']['country']} (now):" + \
                      f" {response['weather'][0]['description']} {emoji_icon}, {response['main']['temp']}ºC ({round(response['main']['temp'] * 1.8 + 32, 2)} ºF), feels like " + \
                      f"{response['main']['feels_like']}ºC, Cloud cover: {response['clouds']['all']}%,Wind: {wind_direction} " + \
                      f"{response['wind']['speed']}m/s. Humidity: {response['main']['humidity']}%," + \
                      f" Pressure: {response['main']['pressure']}hPa, Sunrise: {self.unix_to_time(response['sys']['sunrise'], response['timezone'])}, " + \
                      f" Sunset: {self.unix_to_time(response['sys']['sunset'], response['timezone'])}"
        except Exception as e:
            print(e)
            await ctx.channel.send("Error getting weather data")
            return

        await ctx.channel.send(weather)
        return

    # convert unix time to time of day
    def unix_to_time(self, unix_time, offset) -> str:
        unix_time += int(offset - 3600)
        return datetime.datetime.fromtimestamp(unix_time).strftime("%H:%M:%S")

    # send the respective emoji depending on weather description

    # turn relative degrees to cardinal direction
    def deg_to_cardinal(self, deg) -> str:
        deg = int(deg)
        dirs = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
        ]
        ix = round(deg / (360.0 / len(dirs)))
        return dirs[ix % len(dirs)]

    # save the user's location to mongoDB database
    @commands.command(name="set_location", aliases=['sl'])
    async def set_location(self, ctx, *, msg=None) -> None:
        if msg is None:
            await ctx.channel.send(
                "Please enter a city, or set your location with !set_location"
            )
            return
        coords = self.get_city_coords(msg)
        if coords is None:
            await ctx.channel.send("City not found")
            return
        lat = coords[0]
        lon = coords[1]
        user_id = int(ctx.author.id)
        try:
            await botDB.set_location(
                user_id=user_id, city_name=msg, lat=lat, lon=lon, hidden=False
            )
        except Exception as e:
            print(e)
            await ctx.channel.send("Error saving location")
            return
        await ctx.channel.send("Location set")
        return

    # update user's location
    @commands.command(name="update_location", aliases=["ul"])
    async def update_location(self, ctx, *, msg=None) -> None:
        if msg is None:
            await ctx.channel.send(
                "Please enter a city, or set your location with !set_location"
            )
            return
        coords = self.get_city_coords(msg)
        if coords is None:
            await ctx.channel.send("City not found")
            return
        lat = coords[0]
        lon = coords[1]
        user_id = int(ctx.author.id)
        response = await botDB.update_location(
            user_id=user_id, city_name=msg, lat=lat, lon=lon, hidden=False
        )
        await ctx.channel.send(response)

    def emoji_choice(self, desc) -> str:
        if desc == "clear sky":
            return emoji.emojize(":sunny:", language="alias")
        elif desc == "few clouds":
            return emoji.emojize(":partly_sunny:", language="alias")
        elif desc == "scattered clouds":
            return emoji.emojize(":cloud:", language="alias")
        elif desc == "broken clouds":
            return emoji.emojize(":cloud:", language="alias")
        elif desc == "shower rain" or "rain" in desc:
            return emoji.emojize(":rain_cloud:", language="alias")
        elif desc == "rain":
            return emoji.emojize(":cloud_rain:", language="alias")
        elif desc == "thunderstorm":
            return emoji.emojize(":thunder_cloud_rain:", language="alias")
        elif desc == "snow":
            return emoji.emojize(":snowflake:", language="alias")
        elif desc == "mist":
            return emoji.emojize(":fog:", language="alias")
        elif desc == "overcast clouds":
            return emoji.emojize(":cloud:", language="alias")
        else:
            return emoji.emojize(":sunny:", language="alias")

    @commands.command(name="restart")
    async def restart(self, ctx) -> None:
        if ctx.author.id == os.environ["BOT_OWNER_ID"]:
            await ctx.channel.send("Restarting...")
            sp.call("start /wait pipenv run python bot.py", shell=True)
            pid = os.getpid()
            os.kill(pid, signal.SIGINT)

        # os.execv(sys.executable, ['pipenv'] + sys.argv)
        else:
            await ctx.channel.send("Cheeky, but no :)")

        # cmd_test.restart(os.getpid())
        # await asyncio.sleep(5)
        # ctx.channel.send("We back!")

    # fill message with string
    @commands.command()
    async def fill(self, ctx, *, msg) -> None:
        filled = ""
        while len(filled + msg) < 500:
            filled += msg + " "
        await ctx.channel.send(filled)

    # add trusted users for link moderation
    @commands.command(name="permit", aliases=["p"])
    async def permit(self, ctx, *, msg) -> None:
        if ctx.author.is_broadcaster or ctx.author.is_mod or ctx.author.is_owner:
            # user_id = requests.get(f"https://api.twitch.tv/helix/users?login={msg}").json()["data"][0]["id"]
            if await botDB.add_trusted_user(username=msg):
                if msg not in self.trusted_users:
                    self.trusted_users.append(msg.lower())
            await ctx.channel.send(f"{msg} is now a trusted user!")
        else:
            await ctx.channel.send("You are not allowed to use this command!")

    # get ability from pokepy
    @commands.command(name="ability", aliases=["a"])
    async def ability(self, ctx: commands.Context, *, msg) -> None:
        ability = self.pokemonClient.get_ability(msg).effect_entries
        for key in ability:
            if key.language.name == "en":
                await ctx.channel.send(key.short_effect)
                return

    # get berry from pokepy
    @commands.command(name="berry", aliases=["b"])
    async def berry(self, ctx: commands.Context, *, msg) -> None:
        berry = requests.get(self.pokemonClient.get_berry(msg).item.url).json()["effect_entries"]
        for key in range(0, len(berry)):
            if berry[key]["language"]["name"] == "en":
                await ctx.channel.send(berry[key]["short_effect"])
                return
            # if key.language.name == "en":
            #     await ctx.channel.send(key.short_effect)
            #     return

    # command that sends message as request to openai api
    @commands.command(name="ai", aliases=["openai"])
    async def ai(self, ctx: commands.Context, *, msg) -> None:
        if not self.is_trusted_user(ctx.author.name):
            await ctx.channel.send("You are not allowed to use this command!")
            return
        if msg is None:
            await ctx.channel.send("Please enter a message")
            return
        try:
            response = openai.Completion.create(
                prompt=msg,
                engine="text-davinci-002",
                temperature=1,
                max_tokens=500,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n", " Human:", " AI:"]
            )
            await ctx.channel.send(response["choices"][0]["text"])
        except asyncio.exceptions.TimeoutError as t:
            print(t)
            await ctx.channel.send("OpenAI API timed out")
        except Exception as e:
            print(e)
            await ctx.channel.send("An error has occurred!")

    def is_trusted_user(self, username) -> bool:
        if not self.trusted_users:
            self.trusted_users = botDB.get_trusted_users()
        for user in self.trusted_users:
            if username == user['username']:
                return True
        return False

    async def event_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            time = str(error).split(".", 1)[1].replace("(", '').replace(')', '')
            await ctx.send("Command is on CD, " + time)

    # command to get a word definition from dictionaryapi
    @commands.command(name="define", aliases=["d"])
    async def define(self, ctx: commands.Context, *, msg) -> None:
        if msg is None:
            await ctx.channel.send("Please enter a word")
            return
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{msg}").json()
            if response is None:
                await ctx.channel.send("Word not found")
                return
            await ctx.channel.send(response[0]["meanings"][0]["definitions"][0]["definition"] + "; EXAMPLE: " +
                                   response[0]["meanings"][0]["definitions"][0]["example"])
        except Exception as e:
            print(e)
            await ctx.channel.send("An error has occurred!")

    # command to trade pokemon between two users
    @commands.command(name="trade", aliases=["t"])
    async def trade(self, ctx: commands.Context) -> None:
        await ctx.channel.send("Who do you wish to trade with?")
        response = await self.wait_for('message', predicate=lambda m: m.author == ctx.author, timeout=60)
        print(response)

    # # command to fetch channel
    #     @commands.command(name="channel", aliases=["c"])
    #     async def channel(self, ctx: commands.Context, *, msg):
    #         print(await self.fetch_channel(msg))
    #         print(type(await self.fetch_channel(msg)))
    #         channel = self.get_channel(msg)
    #         await channel.whisper("test")
    #         await ctx.author.send("test")

    @commands.command(name="color")
    async def color(self, ctx: commands.Context, *, msg):
        # print("color")
        # try:
        #     response = requests.get(f"https://api.twitch.tv/helix/users?login={msg}",
        #                             headers={"Client-ID": os.environ["CLIENT_ID"]})
        #                         # headers=f'Client-Id: {os.environ["CLIENT_ID"]}')
        #     print(response.json())
        # except Exception as e:
        #     print("error")
        #     print(e)
        # get all chatters in channel
        chatters = requests.get(f"https://tmi.twitch.tv/group/user/{ctx.channel.name}/chatters").json()["chatters"]
        print(chatters)
        chatters2 = ctx.channel.chatters
        print(chatters2)
        for chatter in chatters2:
            if chatter.name.lower() == msg.lower():
                chatter2 = ctx.channel.get_chatter(msg)
                print(chatter.name, chatter.color)
                print(chatter2.name, chatter2.color)

    async def release(self, ctx: commands.Context):
        await ctx.channel.send("Who do you wish to release?")
        response = await self.wait_for('message', predicate=lambda m: m.author == ctx.author, timeout=60)
        print(response[0].content)

    # command to trade pokemon between 2 users
    @commands.command(name="trade", aliases=["t"])
    async def trade(self, ctx: commands.Context, *, msg=None):
        name1 = ctx.author.name
        id1 = ctx.author.id
        await ctx.channel.send("Who do you wish to trade with?")
        name2 = await self.wait_for('message', predicate=lambda m: ctx.author.name != self.nick and m.author == ctx.author, timeout=60)
        name2 = name2[0].content
        await ctx.channel.send(f"@{name2}, would u like to trade with {name1}?")
        answer = await self.wait_for('message', predicate=lambda m: ctx.author.name != self.nick and m.author.name == name2)
        id2 = answer[0].author.id
        if answer[0].content == "no":
            await ctx.channel.send(f"{name2} did not agree to trade. Trade cancelled")
            return
        await ctx.channel.send(f"@{name1}, which pokemon would you like to trade?")
        mon1 = await self.wait_for('message', predicate=lambda m: ctx.author.name != self.nick and m.author.name == name1, timeout=60)
        mon1 = mon1[0].content
        await ctx.channel.send(f"@{name2}, which pokemon would you like to trade?")
        mon2 = await self.wait_for('message', predicate=lambda m: ctx.author.name != self.nick and m.author.name == name2, timeout=60)
        mon2 = mon2[0].content
        names = [name1, name2]
        await ctx.channel.send(f"Do you both agree to trade {name1}'s {mon1} for {name2}'s {mon2}? (yes/no)")
        for name in names[:]:
            agreement = await self.wait_for('message', predicate=lambda m: ctx.author.name != self.nick and m.author.name in names, timeout=60)
            if agreement[0].content in ("yes", "y"):
                names.remove(agreement[0].author.name)
        if names:
            await ctx.channel.send("One of you did not agree, or prompt timed out (30s), trade cancelled")
            return
        id1 = int(id1)
        id2 = int(id2)
        if await botDB.exchange_pokemon(user_id=id1, pokemon_name=mon1, user_id2=id2, pokemon_name2=mon2, username=name1, username2=name2):
            await ctx.channel.send("Trade successful!")
            return
        else:
            await ctx.channel.send("Trade failed!")
            return


# bot.py
if __name__ == "__main__":
    # bot.pool = bot.loop.run_until_complete (
    #     asyncpg.create_pool (
    #     host=os.environ['DB_HOST'],
    #     port=os.environ['DB_PORT'],
    #     user=os.environ['DB_USER'],
    #     password=os.environ['DB_PASSWORD'],
    #     database=os.environ['DB_NAME']
    # ))
    bot = Bot()
    bot.run()
