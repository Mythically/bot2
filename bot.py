#!/usr/bin/env python3
import asyncio
import datetime
import os, re, beckett.exceptions, twitchio, pokepy, requests, botDB, emoji
import signal
import subprocess as sp
import sys
from asyncio import sleep
from random import randint
import spotify_playing
# from spellchecker import SpellChecker
# from twitchio import Channel, User, Client
import asyncpg
from twitchio.ext import eventsub, commands, pubsub
# from tqdm import tqdm

# some vars


i = 0
pokemonClient = pokepy.V2Client()
# client_disk_cache = pokepy.V2Client(cache='in_disk', cache_location='/temp')
bot = commands.Bot(
    # set up the bot
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)


# bot.py, below bot object
@bot.event()
async def event_ready():
    print(f'Logged into {bot.connected_channels} | {bot.nick}')


@bot.event()
async def event_message(a):
    # print(a.raw_data.name)
    # print(a.user.name)
    # global said_hi
    # if said_hi is False:
    #     await a.channel.send("I'm alive!")
    #     said_hi = True
    # 'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    # if a.author.name.lower() == os.environ['BOT_NICK'].lower():
    #     return
    #
    # await bot.handle_commands(a)
    # if "deez" in a.content.lower():
    #     if "nutz" in a.content.lower():
    #         return
    #     await a.channel.send("nutz")
    if "gift me" in a.content.lower():
        await a.channel.send(f"/timeout {a.author.name} 1m ")
    if 'hello' in a.content.lower():
        await a.channel.send(f"Hi, @{a.author.name}!")
    if a.content:
        global i
        i += 1

        if "messages" in a.content.lower():
            if a.author.name == "themythh":
                await a.channel.send(str(i))
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

@bot.event()
async def event_message(msg):
    if msg.author:
        author = str(msg.author).split()
        words2 = msg.content.split()
        name = msg.author.name.lower()
        if msg.echo:
            return
        user_id = int(msg.author.id)
        await botDB.updateMessages(name, user_id)
        # if "nightbot" in word:
        if "caught" in words2:
            pokemon_name = words2[4].strip("!")
            pokemon = [pokemonClient.get_pokemon(pokemon_name.lower())]
            pokemon_id = pokemon[0].id
            await msg.channel.send(f"Detected pokemon: {pokemon_name}, #{pokemon_id}")
        for word in author:
            if "stream" in word:
                for word in words2:
                    if "hoss" in word and word != "frathoss":
                        await msg.channel.send(f"/ban {word}")
                        await msg.channel.send("Another hoss bites the dust PogChamp")
        if "buy" and "followers" and "viewers" and "primes" in msg.content:
            await msg.channel.send(f"/ban {name}")


# @bot.command(name="user")
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


# @bot.command(name="reason")
# async def reason(ctx, *, msg):
#     await ctx.channel.send(spell_correction(msg))
#

@bot.command(name="test")
async def test(msg):
    print("test")
    await msg.channel.send('test passed!')


@bot.command(name="type")
async def types2(ctx, *, msg):
    pokemon = [pokepy.V2Client().get_pokemon(msg.lower())]
    pokemon_type = ""
    for x in range(len(pokemon[0].types)):
        pokemon_type += pokemon[0].types[x].type.name
        pokemon_type += " "
    await ctx.channel.send(str(pokemon_type))
    # return list(pokemon_type)


@bot.command(name='weak')
async def ww(ctx, *, msg):
    if " " in msg:
        msg = msg.replace(" ", "-")
    typings = ''
    damage = {'4x': [], '2x': [], '1x': [], '0.5x': [], '0.25x': [], '0x': []}
    pokemon = [pokemonClient.get_pokemon(msg.lower())]
    # print(pokemon)
    if pokemon:
        pokemon_type = []
        for x in range(len(pokemon[0].types)):
            pokemon_type.append(pokemon[0].types[x].type.name)
        for j in range(len(pokemon_type)):
            # print(pokemon_type[j])
            typings += pokemon_type[j]
            typings += ' '
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
            response = requests.get(f'https://pokeapi.co/api/v2/type/{typing}')
            fetch = response.json()
            # print(typing)
            for effect, types in fetch['damage_relations'].items():
                if x % 2 != 0:
                    if loop == 0:
                        g += 1
                    test2 = [type['name'] for type in types]
                    # print(test2)
                    if g == 1:
                        for fetch_weak in test2:
                            damage['2x'].append(fetch_weak)

                    if g == 2:
                        for fetch_weak in test2:
                            damage['0.5x'].append(fetch_weak)

                    if g == 3:
                        for fetch_weak in test2:
                            damage['0x'].append(fetch_weak)

                    if loop == 1:
                        g += 1
                        if g == 1:
                            for fetch_weak in test2:
                                if fetch_weak in damage['2x']:
                                    damage['2x'].remove(fetch_weak)
                                    damage['4x'].append(fetch_weak)
                                if fetch_weak not in damage['2x']:
                                    damage['2x'].append(fetch_weak)
                                if fetch_weak in damage['0x']:
                                    damage['2x'].remove(fetch_weak)
                                if fetch_weak in damage['0.5x']:
                                    damage['2x'].remove(fetch_weak)
                                    damage['1x'].append(fetch_weak)

                        if g == 2:
                            for fetch_weak in test2:
                                print(fetch_weak)
                                if fetch_weak not in damage['0.5x']:
                                    damage['0.5x'].append(fetch_weak)
                                if fetch_weak in damage['0x']:
                                    if fetch_weak in damage['2x']:
                                        damage['2x'].remove(fetch_weak)
                                    if fetch_weak in damage['0.5x']:
                                        damage['0.5x'].remove(fetch_weak)
                                if fetch_weak in damage['2x']:
                                    print(fetch_weak + 'in 2x')
                                    damage['2x'].remove(fetch_weak)
                                    if fetch_weak in damage['2x']:
                                        damage['2x'].remove(fetch_weak)

                                    print(damage['2x'])

                        if g == 3:
                            for fetch_weak in test2:
                                if fetch_weak in damage['4x']:
                                    damage['4x'].remove(fetch_weak)
                                elif fetch_weak in damage['2x']:
                                    damage['2x'].remove(fetch_weak)

                x += 1
            loop += 1

    for type in damage['0x']:
        for type in damage['0x']:
            if type in damage['2x']:
                damage['2x'].remove(type)
        if type in damage['4x']:
            damage['4x'].remove(type)
    for type in damage['2x']:
        if type in damage['4x']:
            damage['2x'].remove(type)

    message1 = ''
    message2 = ''
    if damage['4x']:
        message1 = ', '.join(damage['4x'])
        # for x in range(len(damage['4x'])):
        #     message += damage['4x'][x]
    if damage['2x']:
        message2 = ', '.join(damage['2x'])

    if message1:
        await ctx.channel.send(pokemon[0].name + ' is: ' + typings + ' takes 4x: ' + message1 + '; 2x: ' + message2)
        return
    await ctx.channel.send(pokemon[0].name + ' is: ' + typings + ' takes 2x: ' + message2)


@bot.command(name="w")
async def weak_type(ctx, *, msg):
    damage = {'4x': [], '2x': [], '1x': [], '0.5x': [], '0.25x': [], '0x': []}
    pokemon_type = msg.split()
    x = 1
    loop = 0
    if pokemon_type:
        for typing in pokemon_type:

            g = 0
            # print('loop')
            response = requests.get(f'https://pokeapi.co/api/v2/type/{typing}')
            fetch = response.json()
            # print(typing)
            for effect, types in fetch['damage_relations'].items():
                if x % 2 != 0:
                    if loop == 0:
                        g += 1
                    test2 = [type['name'] for type in types]
                    # print(test2)
                    if g == 1:
                        for fetch_weak in test2:
                            damage['2x'].append(fetch_weak)

                    if g == 2:
                        for fetch_weak in test2:
                            damage['0.5x'].append(fetch_weak)

                    if g == 3:
                        for fetch_weak in test2:
                            damage['0x'].append(fetch_weak)

                    if loop == 1:
                        g += 1
                        if g == 1:
                            for fetch_weak in test2:
                                if fetch_weak in damage['2x']:
                                    damage['2x'].remove(fetch_weak)
                                    damage['4x'].append(fetch_weak)
                                if fetch_weak not in damage['2x']:
                                    damage['2x'].append(fetch_weak)
                                if fetch_weak in damage['0x']:
                                    damage['2x'].remove(fetch_weak)
                                if fetch_weak in damage['0.5x']:
                                    damage['2x'].remove(fetch_weak)
                                    damage['1x'].append(fetch_weak)

                        if g == 2:
                            for fetch_weak in test2:
                                print(fetch_weak)
                                if fetch_weak not in damage['0.5x']:
                                    damage['0.5x'].append(fetch_weak)
                                if fetch_weak in damage['0x']:
                                    if fetch_weak in damage['2x']:
                                        damage['2x'].remove(fetch_weak)
                                    if fetch_weak in damage['0.5x']:
                                        damage['0.5x'].remove(fetch_weak)
                                if fetch_weak in damage['2x']:
                                    print(fetch_weak + 'in 2x')
                                    damage['2x'].remove(fetch_weak)
                                    if fetch_weak in damage['2x']:
                                        damage['2x'].remove(fetch_weak)

                                    print(damage['2x'])

                        if g == 3:
                            for fetch_weak in test2:
                                if fetch_weak in damage['4x']:
                                    damage['4x'].remove(fetch_weak)
                                elif fetch_weak in damage['2x']:
                                    damage['2x'].remove(fetch_weak)

                x += 1
            loop += 1

    for type in damage['0x']:
        for type in damage['0x']:
            if type in damage['2x']:
                damage['2x'].remove(type)
        if type in damage['4x']:
            damage['4x'].remove(type)
    for type in damage['2x']:
        if type in damage['4x']:
            damage['2x'].remove(type)

    message = ''
    if damage['4x']:
        message += '4x: ' + str(damage['4x'])
        # for x in range(len(damage['4x'])):
        #     message += damage['4x'][x]
    if damage['2x']:
        message += ' 2x: ' + str(damage['2x'])

    await ctx.channel.send(str(message))


@bot.command(name="trigger")
async def trigger(ctx, *, msg):
    if msg.isnumeric() is True:
        pokemon_id = msg
    elif msg.isnumeric() is False:
        pokemon = [pokemonClient.get_pokemon(msg.lower())]
        pokemon_id = pokemon[0].id
        print(pokemon, pokemon_id)
    pokemon = [pokemonClient.get_pokemon(msg.lower())]
    # print(pokemon_id)
    id = [pokemonClient.get_pokemon_species(pokemon_id)]
    pokemon_species_id = id[0].evolution_chain.url
    pokemon_evolution_id = pokemon_species_id.split("/")[-2]
    pokemon_evolution = [pokemonClient.get_evolution_chain(pokemon_evolution_id)]
    # print(str(pokemon_species_id) + " chain")
    # print(pokemon_evolution_id)
    # pokemon_trigger = pokemon_evolution[0].chain.evolves_to[0].evolution_details[0].trigger.name
    # print(pokemon_trigger)
    # pokemon_evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolution_details
    pokemon_name1 = pokemon_evolution[0].chain.species.name
    pokemon_name2 = pokemon_evolution[0].chain.evolves_to[0].species.name
    pokemon_name3 = pokemon_evolution[0].chain.evolves_to[0].evolves_to[0].species.name
    # print(msg)
    # print(pokemon[0].name)
    # print(pokemon_name1 + "1st evolution")
    # print(pokemon_name2 + "2nd evolution")
    pokemon_message = ' '
    if pokemon[0].name == pokemon_name1:
        evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolution_details[0]
        pokemon_message += pokemon[0].name + " -> " + pokemon_name2 + "; "
    elif pokemon[0].name == pokemon_name2:
        evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolves_to[0].evolution_details[0]
        pokemon_message += pokemon[0].name + " -> " + pokemon_name3 + "; "
    elif pokemon[0].name == pokemon_name3:
        await ctx.channel.send(f"{pokemon[0].name} doesn't evolve AFAIK :3")

    else:
        evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolves_to[0].evolution_details[0]
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
        pokemon_message += "Needs to know a move:   " + str(trigger_move).replace("<Named_API_Resource |", "").replace(
            ">", "")
    if trigger_move_type is not None:
        pokemon_message += "Needs to know a move of type: " + str(trigger_move_type)
    if trigger_item is not None:
        pokemon_message += "Needs an item to evolve: " + str(trigger_item.name)
    if trigger_held_item is not None:
        pokemon_message += "Needs to hold item to evolve: " + str(trigger_held_item)

    if pokemon_message == ' ':
        await ctx.channel.send("Another evolution trigger that I have not accounted for yet, please bare with me :3")
        return
    await ctx.channel.send(pokemon_message)


@bot.command(name="move")
async def move(ctx, *, msg):
    # ctx.channel.send(msg)
    if " " in msg:
        msg = msg.replace(" ", "-")
    # print(msg)
    move = [pokemonClient.get_move(msg)]
    type = str(move[0].type.name)
    damage_class = str(move[0].damage_class.name)
    power = str(move[0].power)
    pp = str(move[0].pp)
    priority = str(move[0].priority)
    effect_entries = str(move[0].effect_entries[0].effect)
    effect_chance = str(move[0].effect_chance)
    await ctx.channel.send(
        type + "; " + damage_class + " Power: " + power + " PP: " + pp + " Priority: " + priority + "  " + effect_entries.replace(
            " $effect_chance", effect_chance))


@bot.command(name="vanish")
async def time_outed(msg):
    if msg.author.name != bot.nick:
        print(f"/timeout {msg.author.name}")
        await msg.channel.send(f"/timeout {msg.author.name} 1s")


# @bot.command(name='resets')
# async def resets(msg):
#     await msg.channel.send('0 resets baby, THIS IS THE RUN LETSGO !!!!')

@bot.command(name="kill")
async def kill(msg):
    print(msg.channel.name)

    if msg.author.is_broadcaster or msg.author.name == "themythh" or msg.author.is_mod:
        await msg.channel.send("Bye! :)")
        await bot.close()


@bot.command(name="timer")
async def timer(ctx, *, msg):
    if 's' in msg:
        msg = msg[:-1]
    if 'm' in msg:
        msg = msg[:-1]
        msg = int(msg)
        msg *= 60
    if int(msg) > 0:
        mins = int(msg) / 60
        secs = str(int(msg) % 60) + "s"
        hours = mins / 60
        hours = str(round(hours)) + "h"
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
        await ctx.channel.send("Timer of " + hours + mins + secs + ", just ran out!")


@bot.command(name="ryan")
async def ryan(msg):
    await msg.channel.send("FeelsAmazingMan oiler")


@bot.command(name="lag")
async def lag(msg):
    if msg.author.name == "themythh":
        while True:
            await sleep(1)
            await msg.channel.send("SourPls LAG THE CHAT SourPls ")


@bot.command(name="so")
async def so(ctx, *, msg):
    await ctx.channel.send("Yo what are you waiting for, go check out " + msg + " at www.twitch.tv/" + msg)


@bot.command(name="dance")
async def dance(msg):
    if msg.author.name == "themythh":
        while True:
            await sleep(5)
            await msg.channel.send("SourPls")


@bot.command(name="brain")
async def dance(msg):
    if msg.author.name == "themythh":
        while True:
            await sleep(1)
            await msg.channel.send(
                "/me O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee "
                "AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA ")


@bot.command(name="coinflip", aliases=['cf'])
async def coinflip(msg):
    number = randint(1, 2)
    if number == 1:
        await msg.channel.send("It landed on HEADS")
    else:
        await msg.channel.send("It landed on TAILS")


@bot.command(name="killskygod")
async def killskygod(msg):
    await msg.channel.send("/ban RollingSkyGod")


@bot.command(name="saveskygod")
async def saveskygod(msg):
    await msg.channel.send("/unban RollingSkyGod")


# @bot.command(name="reset", aliases=["t"])
# async def reset(ctx, *, msg):
#     if reset in msg:
#         await bot.close()
#         await bot.join_channels([ctx.channel.name])

# @bot.command(name='brain')
# async def brian(msg):
#     while True:
#         await sleep(0.5)
#         await msg.channel.send('/me  O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA ')

@bot.command(name="join")
async def join(ctx, *, msg):
    channel_name = [msg]
    await bot.join_channels(channel_name)
    await ctx.channel.send("Joined channel: " + str(channel_name))
    print(channel_name)


@bot.command(name="leave")
async def leave(ctx):
    channel_name = ctx.channel.name
    await bot.part_channels[channel_name]


@bot.command(name="mon")
async def pokemon(ctx):
    try:
        pokemon_id = randint(0, 1126)
        pokemon = pokemonClient.get_pokemon(pokemon_id)
        pokemon_name = pokemon.forms[0].name
        link_pokemon_name = pokemon_name.split("-")
        link_pokemon_name = str(link_pokemon_name[0]).strip("[").strip("]").strip("\'")
        link = f"https://pokemondb.net/pokedex/{link_pokemon_name}"
        await botDB.insertCaughtPokemon(int(pokemon_id), pokemon_name, int(ctx.author.id), ctx.author.name)
        await ctx.channel.send(
            "@" + str(ctx.author.name) + ' you\'ve caught a ' + str(
                pokemon_name.capitalize()) + "! " + link + ' Gotta catch \'em all!')
    except beckett.exceptions.InvalidStatusCodeError as e:
        print(e)
        await ctx.channel.send(str(await botDB.getEscapePhrase()))


@bot.command(name="pokedex")
async def pokedex(ctx, *, msg=None):
    if msg == "deviation":
        mons = await botDB.getPokedex(ctx.author.name)
        spread = {}
        total = 0
        check = 0
        for mon in mons:
            first_letter = mon['pokemon_name'][0]
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
    mons = await botDB.getPokedex(msg)
    if len(mons) == 0:
        await ctx.channel.send("No pokemon found, use !mon to catch one!")
        return
    for mon in mons:
        if len(pokemons + mon['pokemon_name'] + ", ") < 500:
            pokemons += mon['pokemon_name'] + ", "
        if len(pokemons + mon['pokemon_name'] + ", ") > 500:
            await ctx.channel.send(pokemons)
            pokemons = ""
            await sleep(1)

    await ctx.channel.send("Your pokedex has: " + pokemons)


@bot.command(name="ban")
async def ban(msg):
    for x in range(1, 10000):
        await sleep(0.3)
        await msg.channel.send(f'/ban hoss{x}')
        await sleep(0.3)
        await msg.channel.send(f'/ban hossoo_{x}')
        await sleep(0.3)
        await msg.channel.send(f'/ban hoss00{x}')
        await sleep(0.3)
        await msg.channel.send(f'/ban hoss000{x}')
        await sleep(0.3)
        await msg.channel.send(f'/ban h0ssoo{x}')
        await sleep(0.3)
        await msg.channel.send(f'/ban h0ss__{x}')
        await sleep(0.3)
        await msg.channel.send(f'/ban hoss__{x}')
        await sleep(0.3)
        await msg.channel.send(f'/ban hoss00{x}__')
        await sleep(0.3)


@bot.command(name='ban2')
async def banTXT(ctx):
    file = open('ban.txt', 'r')
    # count = 0
    for line in file:
        # count += 1
        # if count > 600:
        await sleep(2)
        await ctx.channel.send(f'{line.strip()}')
    file.close()


# @bot.command()
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


# @bot.command(name="leave")
# async def leave(ctx, *, msg):
#     channel_name = [msg]
#     await bot.

@bot.command()
async def bttvemotes(ctx, *, msg=None):
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


@bot.command(name="7tvemotes")
async def seventvemotes(ctx, *, msg=None):
    if msg is None:
        print(msg, ctx.channel.name)
        msg = ctx.channel.name
    emotesString = ""
    counter = 0
    response = requests.get(f"https://api.7tv.app/v2/users/{msg}/emotes")
    fetch = response.json()
    for numbers, word in enumerate(fetch):
        # print(word['name'])
        if len(emotesString + word['name']) < 500:
            emotesString += word['name'] + " "
            counter += 1
        if (len(emotesString + word['name']) > 500) or (numbers == len(fetch) - 1):
            await ctx.channel.send(emotesString)
            emotesString = ""
            counter = 0
            await sleep(2)


@bot.command()
async def ffzemotes(ctx, *, msg=None):
    emoteString = ""
    if msg is None:
        print(msg, ctx.channel.name)
        msg = ctx.channel.name

    response = requests.get("https://api.frankerfacez.com/v1/room/" + msg)
    fetch = response.json()
    for account, id in fetch['sets'].items():
        for emoticon in id['emoticons']:
            emoteString += str(emoticon['name'] + " ")
    await ctx.channel.send(emoteString)


def ffzemotes2(msg):
    emoteString = ""
    response = requests.get("https://api.frankerfacez.com/v1/room/" + msg)
    fetch = response.json()

    for account, id in fetch['sets'].items():
        for emoticon in id['emoticons']:
            emoteString += str(emoticon['name'] + " ")
    return emoteString


@bot.command(name="song")
async def spotify_current_song(ctx):
    if botDB.checkIfAlreadyInserted(ctx.channel.name):
        current_song = spotify_playing.get_song(ctx.channel.name, ctx.channel)
        await ctx.channel.send(current_song)
    else:
        await ctx.channel.send("It seems that this channel has not yet linked their spotify, please check with the "
                               "broadcaster.")


@bot.command(name="spotify")
async def spotify_token(ctx):
    await ctx.channel.send("You can sign up here :) -> https://accounts.spotify.com/authorize?client_id"
                           "=90082084b6b6423f8f08dd85e74f42b4&response_type=code&redirect_uri=https://b816-103-219-21"
                           "-123.eu.ngrok.io/&scope=user-read-currently-playing")


@bot.command(name="checkKey")
async def checkSpotifyToken(ctx):
    await ctx.channel.send(botDB.checkSpotifyRefreshToken(ctx.author.name))


async def send_message(msg, channel):
    await channel.send(msg)


@bot.command(name="sayfile")
async def sayfile(ctx, *, msg):
    response = requests.get(f"{msg}")
    bans = response.text.split("\n")
    print(bans, type(bans))
    for line in bans:
        await ctx.channel.send(str(line))
        await sleep(0.3)


@bot.command()
async def pyramid(ctx, *, msg):
    new = msg.split(" ")
    limit = 5
    if ctx.author.is_broadcaster:
        limit = 48
        await ctx.channel.send("You are strimermans Pog")
    if not str(new[1]).isnumeric():
        await ctx.channel.send(f"Does \"{new[1]}\" look like a number to you!? Madge ")
        return
    x = int(new[1])

    if x > limit and ctx.author.name == "ws_zoomers":
        await ctx.channel.send(f"{limit} is the limit, you are asking for {x}")
        await ctx.channel.send("I know it's fun, but chill out")
        return
    column = ""

    for rows in range(x):
        column += new[0] + " "
        if len(column) > 500:
            await ctx.channel.send("Message is longer than 500 characters")
            return
        await ctx.channel.send(column)
    column = column.rsplit(' ', 1)[0]

    for row in range(x - 1, 0, -1):
        column = column.rsplit(' ', 1)[0]
        await ctx.channel.send(column)


@bot.command(name="r")
async def randd(ctx, *, msg="None"):
    number = randint(1, 3)
    await ctx.channel.send(str(number))


# @bot.command()
# async def weather(ctx, *, msg):
#     link = ""
#     api_key = os.environ['OPENWEATHER_API_KEY']
#     result = requests.get(link + msg)


# @bot.command(name="weather")
# async def weather(ctx, *, msg):
#     result = requests.get("")

@bot.command()
async def dia(ctx, *, msg=None):
    if msg is None:
        await ctx.channel.send("Please send a message")
    # response = (await bot.wait_for('message', predicate=lambda m: m.author == ctx.author))
    await ctx.channel.send(msg)


@bot.command()
async def fog(ctx):
    await ctx.channel.send(emoji.emojize(":fog:", use_aliases=True))


@bot.command(name="fact")
async def facts(ctx, *, msg=None):
    if msg is None:
        facts = ["random/math", "random/trivia", "random/year", "random/date"]
        number = randint(0, 3)
        await ctx.channel.send(requests.get("http://numbersapi.com/" + facts[number]).text)


@bot.command(name="8ball")
async def eight_ball(ctx, *, msg=None):
    if msg is None:
        await ctx.channel.send("Please ask a question")
        return
    answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "You may rely on it",
               "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again",
               "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
               "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
    await ctx.channel.send(answers[randint(0, len(answers) - 1)])


# use pokeapi.com to get pokemon info
# messages should be less than 500 characters
@bot.command(name="pokemon")
async def pokemon(ctx, *, msg=None):
    if msg is None:
        await ctx.channel.send("Please enter a pokemon name")
        return
    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + msg)
    if response.status_code == 404:
        await ctx.channel.send("Pokemon not found")
        return
    response = response.json()
    await ctx.channel.send(
        f"{response['name']} is a {response['height']} tall {response['weight']} heavy {response['types'][0]['type']['name']}")
    await ctx.channel.send(f"{response['abilities'][0]['ability']['name']}")
    await ctx.channel.send(f"{response['stats'][5]['base_stat']}")
    await ctx.channel.send(f"{response['stats'][4]['base_stat']}")
    await ctx.channel.send(f"{response['stats'][3]['base_stat']}")
    await ctx.channel.send(f"{response['stats'][2]['base_stat']}")
    await ctx.channel.send(f"{response['stats'][1]['base_stat']}")
    await ctx.channel.send(f"{response['stats'][0]['base_stat']}")
    await ctx.channel.send(f"{response['sprites']['front_default']}")
    await ctx.channel.send(f"{response['sprites']['front_shiny']}")
    await ctx.channel.send(f"{response['sprites']['back_default']}")
    await ctx.channel.send(f"{response['sprites']['back_shiny']}")


# use pokepy to decide what types are strong against each other in one message
# message length should be less than 500 characters
# verify if list index is out of range
@bot.command(name="types")
async def types(ctx, *, msg=None):
    if msg is None:
        await ctx.channel.send("Please enter a type")
        return
    response = requests.get("https://pokeapi.co/api/v2/type/" + msg)
    if response.status_code == 404:
        await ctx.channel.send("Type not found")
        return
    response = response.json()
    await ctx.channel.send(
        f"{response['name']} is weak to: {response['damage_relations']['double_damage_from'][0]['name']}")
    await ctx.channel.send(
        f"{response['name']} is strong against: {response['damage_relations']['double_damage_to'][0]['name']}")
    await ctx.channel.send(
        f"{response['name']} is immune to: {response['damage_relations']['no_damage_from'][0]['name']}")
    await ctx.channel.send(
        f"{response['name']} is weak to: {response['damage_relations']['half_damage_from'][0]['name']}")
    await ctx.channel.send(
        f"{response['name']} is resistant against: {response['damage_relations']['half_damage_to'][0]['name']}")
    await ctx.channel.send(
        f"{response['name']} is deals no damage to: {response['damage_relations']['no_damage_to'][0]['name']}")


# return long and lat of a city using openweathermap direct geocoding
# save city name and long and lat to sql database
def get_city_coords(city_name):
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=" + os.environ[
            'OPENWEATHERMAP_API_KEY'])
    if response.status_code == 404:
        return "Could not find city"
    response = response.json()
    return response['coord']['lat'], response['coord']['lon']


# use coords_city() to get the weather of a city from openweathermap 2.5 api
@bot.command(name="weather")
async def weather(ctx, *, msg=None):
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
        coords = get_city_coords(msg)
        if coords == "Could not find city":
            await ctx.channel.send("Couldn't get city coordinates. Please check spelling and try again.")
            return
        lat = coords[0]
        lon = coords[1]
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid="
        f"{os.environ['OPENWEATHERMAP_API_KEY']}&units=metric")
    if response.status_code == 404:
        await ctx.channel.send("City not found")
        return
    response = response.json()
    emoji_icon = emoji_choice(response['weather'][0]['description'])
    wind_direction = deg_to_cardinal(response['wind']['deg'])

    await ctx.channel.send(
        f"{ctx.author.name}, {response['name']},{response['sys']['country']} (now):"
        f" {response['weather'][0]['description']} {emoji_icon}, {response['main']['temp']}ºC feels like "
        f"{response['main']['feels_like']}ºC, Cloud cover: {response['clouds']['all']}%,Wind: {wind_direction} "
        f"{response['wind']['speed']}m/s. Humidity: {response['main']['humidity']}%,"
        f" Pressure: {response['main']['pressure']}hPa, Sunrise: {unix_to_time(response['sys']['sunrise'])},"
        f" Sunset: {unix_to_time(response['sys']['sunset'])}")


# convert unix time to time of day
def unix_to_time(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%H:%M:%S')


# send the respective emoji depending on weather description
def emoji_choice(desc):
    if desc == "clear sky":
        return emoji.emojize(":sunny:", language='alias')
    elif desc == "few clouds":
        return emoji.emojize(":partly_sunny:", language='alias')
    elif desc == "scattered clouds":
        return emoji.emojize(":cloud:", language='alias')
    elif desc == "broken clouds":
        return emoji.emojize(":cloud:", language='alias')
    elif desc == "shower rain":
        return emoji.emojize(":rain_cloud:", language='alias')
    elif desc == "rain":
        return emoji.emojize(":cloud_rain:", language='alias')
    elif desc == "thunderstorm":
        return emoji.emojize(":thunder_cloud_rain:", language='alias')
    elif desc == "snow":
        return emoji.emojize(":snowflake:", language='alias')
    elif desc == "mist":
        return emoji.emojize(":fog:", language='alias')
    elif desc == "overcast clouds":
        return emoji.emojize(":cloud:", language='alias')
    else:
        return emoji.emojize(":sunny:", language='alias')


# turn relative degrees to cardinal direction
def deg_to_cardinal(deg):
    deg = int(deg)
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = round(deg / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


# save the user's location to mongoDB database
@bot.command(name="set_location")
async def set_location(ctx, *, msg=None):
    if msg is None:
        await ctx.channel.send("Please enter a city, or set your location with !set_location")
        return
    coords = get_city_coords(msg)
    if coords is None:
        await ctx.channel.send("City not found")
        return
    lat = coords[0]
    lon = coords[1]
    user_id = int(ctx.author.id)
    try:
        await botDB.set_location(user_id=user_id, city_name=msg, lat=lat, lon=lon, hidden=False)
    except Exception as e:
        print(e)
        await ctx.channel.send("Error saving location")
        return
    await ctx.channel.send("Location set")


#update user's location
@bot.command(name="update_location", aliases=["ul"])
async def update_location(ctx, *, msg=None):
    if msg is None:
        await ctx.channel.send("Please enter a city, or set your location with !set_location")
        return
    coords = get_city_coords(msg)
    if coords is None:
        await ctx.channel.send("City not found")
        return
    lat = coords[0]
    lon = coords[1]
    user_id = int(ctx.author.id)
    response = await botDB.update_location(user_id=user_id, city_name=msg, lat=lat, lon=lon, hidden=False)#
    await ctx.channel.send(response)


@bot.command(name="restart")
async def restart(ctx):
    if ctx.author.id == os.environ['BOT_OWNER_ID']:
        await ctx.channel.send("Restarting...")
        sp.call('start /wait pipenv run python bot.py', shell=True)
# os.execv(sys.executable, ['pipenv'] + sys.argv)
    else:
        await ctx.channel.send("Cheeky, but no :)")

    # cmd_test.restart(os.getpid())
    # await asyncio.sleep(5)
    # ctx.channel.send("We back!")

#fill message with string
@bot.command()
async def fill(ctx, *, msg):
    filled = ""
    while len(filled + msg) < 500:
        filled += msg + " "
    await ctx.channel.send(filled)


# bot.py
if __name__ == "__main__":
    # bot.pool = bot.loop.run_until_complete(asyncpg.create_pool(
    #     host=os.environ['DB_HOST'],
    #     port=os.environ['DB_PORT'],
    #     user=os.environ['DB_USER'],
    #     password=os.environ['DB_PASSWORD'],
    #     database=os.environ['DB_NAME']
    # ))
    bot.run()
