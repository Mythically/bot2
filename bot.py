# import asyncio
import os  # for importing env vars for the bot to use
from asyncio import sleep
# from multiprocessing import get_context
# from pickletools import string1
from random import randint
# from pprint import pprint
# import pubSub
import twitchio
import pokepy
# import json
import requests
# from requests import get
from spellchecker import SpellChecker
from twitchio import Channel, User, Client
from twitchio.ext import eventsub, commands, pubsub
import botDB
from tqdm import tqdm
# from pprint import pprint

# setting up database connection
# myClient = pymongo.MongoClient("mongodb://localhost:27017/")
# admin = myClient.admin
# serverStatusResult=admin.command("serverStatus")
# pprint(serverStatusResult)
# botDB = myClient["botDatabase"]
# chatUsers = botDB["users"]
# userDict = [""]

# some vars
import spotify_playing

i = 0
words = ''
spell = SpellChecker(language='en')
pokemonClient = pokepy.V2Client()
# client_disk_cache = pokepy.V2Client(cache='in_disk', cache_location='/temp')
said_hi = False
my_token = os.environ["TMI_TOKEN"]
users_oauth_token = "se4xwnmyhahz1us708e7z3zasp8j9y"
users_channel_id = 50458406
client = twitchio.Client(token=my_token)
client.pubsub = pubsub.PubSubPool(client)
topic = [pubsub.bits(users_oauth_token)[users_channel_id]]

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
    author = str(msg.author).split()
    words2 = msg.content.split()
    botDB.incMessages(msg.author.name.lower())
    # if "nightbot" in word:
    if "caught" in words2:
        pokemon_name = words2[4].strip("!")
        pokemon = [pokemonClient.get_pokemon(pokemon_name.lower())]
        pokemon_id = pokemon[0].id
        await msg.channel.send(f"Detected pokemon: {pokemon_name}, #{pokemon_id}")
    for word in author:
        if "stream" in word:
            for word in words:
                if "hoss" in word and word != "frathoss":
                    await msg.channel.send(f"/ban {word}")
                    await msg.channel.send("Another hoss bites the dust PogChamp")
    if "buy" and "followers" and "viewers" and "primes" in msg.content:
        await msg.channel.send("banned")


# @bot.command(name="user")
# async def users(msg):
#     response = requests.get("https://api.twitch.tv/helix/users?login=zack_ko")
#     fetch = response.json()
#     print(fetch)


@client.event()
async def event_raw_usernotice(channel: Channel, tags: dict):
    print("Channel " + str(channel) + " tags " + str(tags))
    listing = tags.items()
    stringify = ""
    for item in range(len(listing)):
        stringify += item

    print("TAGS: " + stringify)
    if "first-msg" in tags:
        await channel.send("First message")


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


@bot.command(name="type", aliases=['t'])
async def types2(ctx, *, msg):
    pokemon = [pokepy.V2Client().get_pokemon(msg.lower())]
    pokemon_type = ""
    for x in range(len(pokemon[0].types)):
        pokemon_type += pokemon[0].types[x].type.name
        pokemon_type += " "
    await ctx.channel.send(str(pokemon_type))
    # return list(pokemon_type)

@bot.command(name='weak', aliases=['t'])
async def ww(ctx, *, msg):
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


@bot.command(name="w", aliases=['t'])
async def w(ctx, *, msg):
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


@bot.command(name="trigger", aliases=['t'])
async def trigger(ctx, *, msg):
    if msg.isnumeric() is True:
        pokemon_id = msg
    elif msg.isnumeric() is False:
        pokemon = [pokemonClient.get_pokemon(msg.lower())]
        pokemon_id = pokemon[0].id
        print(pokemon, pokemon_id)
    pokemon = [pokemonClient.get_pokemon(msg.lower())]
    # print(pokemon_id)
    # await ctx.channel.send(chain[0].chain.evolves_to.species.name)
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
    # print(msg)
    # print(pokemon[0].name)
    # print(pokemon_name1 + "1st evolution")
    # print(pokemon_name2 + "2nd evolution")
    if pokemon[0].name == pokemon_name1:
        evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolution_details[0]

    elif pokemon[0].name == pokemon_name2:
        evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolves_to[0].evolution_details[0]

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
    pokemon_message = ' '
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
        pokemon_message += "Needs to know a move:" + str(trigger_move)
    if trigger_move_type is not None:
        pokemon_message += "Needs to know a move of type: " + str(trigger_move_type)
    if trigger_item is not None:
        pokemon_message += "Needs the item to evolve: " + str(trigger_item.name)
    if trigger_held_item is not None:
        pokemon_message += "Needs to hold item to evolve: " + str(trigger_held_item)

    if pokemon_message == ' ':
        await ctx.channel.send("Another evolution trigger that I have not accounted for yet, please bare with me :3")
        return
    await ctx.channel.send(pokemon_message)


# @bot.command(name="add", aliases=['t'])
# async def add(ctx, *, msg):
#     message = msg.split()
#     user = ctx.author.name
#     query = {'_id': message[0], 'pokemon': {message[1]: True}}
#     botDB.insert(query)


@bot.command(name="adddeath", aliases=['t'])
async def adddeath(ctx, *, msg):
    botDB.setDeathMsg(msg)


@bot.command(name="deathlog", aliases=['t'])
async def deathLog(ctx):
    msg = botDB.getRandDeathMsg()
    await ctx.channel.send(msg)


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
    await msg.channel.send("Bye! :)")
    print(msg.channel.name)

    if msg.author.name == msg.channel.name or msg.author.name == "themythh":
        await bot.close()


@bot.command(name="timer", aliases=['t'])
async def timer(ctx, *, msg):
    if 's' in msg:
        msg = msg[:-1]
    if 'm' in msg:
        msg = msg[:-1]
        msg = int(msg)
        msg *= 60
    if int(msg) > 0:
        minutes = int(msg) / 60
        print("send")
        await ctx.channel.send("Timer " + str(minutes) + "started :)")
        await sleep(int(msg))
        await ctx.channel.send("Timer of " + str(minutes) + " min, just ran out!")


@bot.command(name="ryan")
async def timer(msg):
    await msg.channel.send("FeelsAmazingMan oiler")


@bot.command(name="lag")
async def lag(msg):
    if msg.author.name == "themythh":
        while True:
            await sleep(1)
            await msg.channel.send("SourPls LAG THE CHAT SourPls ")


@bot.command(name="so", aliases=['t'])
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


@bot.command(name="coinflip")
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

@bot.command(name="join", aliases=['t'])
async def join(ctx, *, msg):
    channel_name = [msg]
    await bot.join_channels(channel_name)
    await ctx.channel.send("Joined channel: " + str(channel_name))
    print(channel_name)


@bot.command(name="ban")
async def ban(msg):
    for x in range(1, 10000):
        await sleep(2)
        await msg.channel.send(f'/ban hoss{x}')
        await sleep(2)
        await msg.channel.send(f'/ban hossoo_{x}')
        await sleep(2)
        await msg.channel.send(f'/ban hoss00{x}')
        await sleep(2)
        await msg.channel.send(f'/ban hoss000{x}')
        await sleep(2)
        await msg.channel.send(f'/ban h0ssoo{x}')
        await sleep(2)
        await msg.channel.send(f'/ban h0ss__{x}')
        await sleep(2)
        await msg.channel.send(f'/ban hoss__{x}')
        await sleep(2)
        await msg.channel.send(f'/ban hoss00{x}__')
        await sleep(2)


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


# @bot.command(name="leave", aliases=['t'])
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


@bot.command(name="song")
async def spotify_current_song(ctx):
    current_song = spotify_playing.get_song("themythh", ctx.channel)
    await ctx.channel.send(current_song)


def spell_check(word):
    global spell, words

    misspelled = spell.unknown(word)
    for word in misspelled:
        words += word + ' '
    return words


@bot.command(name="spotify")
async def spotifyToken(ctx, *, msg):
    await ctx.channel.send(botDB.insetSpotifyRefreshToken(ctx.author.channel.name, msg))


@bot.command(name="checkKey")
async def checkSpotifyToken(ctx):
    await ctx.channel.send(botDB.checkSpotifyRefreshToken(ctx.author.name))


async def send_message(msg, channel):
    await channel.send(msg)


def spell_correction(word):
    return spell.correction(word)


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


# bot.py
if __name__ == "__main__":
    bot.run()
