#!/usr/bin/env python3
import asyncio
import time
from pprint import pprint

import asyncpg
import openai
import pokepy
from bs4 import BeautifulSoup

import botDB
import datetime
import emoji
import math
import os
import re
import requests
from datetime import datetime
from asyncio import sleep
from random import randint
# from spellchecker import SpellChecker
# from twitchio import Channel, User, Client
from twitchio.ext import commands, routines

# import spotify_playing
from cogs import pokedex


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
    pokemonClient = pokepy.V2Client(cache="in_disk", cache_location="./cache")
    trusted_users: list = []
    initial_extensions: list = ["cogs.pokemon", "cogs.pokedex"]
    reminders: list = []

    async def event_ready(self) -> None:
        print(f"Logged into {self.connected_channels} | {self.nick}")
        # self.trusted_users = await botDB.get_trusted_users()
        for channel in self.connected_channels:
            print(channel)
            await channel.send("I am online!")
        for cog in self.initial_extensions:
            print(cog)
            self.load_module(cog)

    async def event_message(self, msg) -> None:
        if msg.echo:
            return

        for reminder in self.reminders:
            print(reminder['for'])
            if reminder['for'] == msg.author.name:
                await msg.channel.send(f"@{msg.author.name} reminder from {reminder['sender']}: {reminder['message']}")
                self.reminders.remove(reminder)
        await self.handle_commands(msg)
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

        if (
                self.is_trusted_user(msg.author.name)
                or msg.author.is_mod
                or msg.author.is_subscriber
                or msg.author.is_broadcaster
        ):
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
            if (
                    "buy" in msg.content
                    and "followers" in msg.content
                    and "viewers" in msg.content
                    and "primes" in msg.content
            ):
                await msg.channel.send(f"/ban {name}")

    @commands.command(name="test")
    async def test(self, msg) -> None:
        print("test")
        await msg.channel.send("test passed!")

    @commands.command(name="vanish")
    async def time_outed(self, msg) -> None:
        if msg.author.name != bot.nick:
            print(f"/timeout {msg.author.name}")
            await msg.channel.send(f"/timeout {msg.author.name} 1s")

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
            mins %= 60
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
            + msg
            + "they were last playing"
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

    @commands.command(name="goto")
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


    # @commands.command(name="song")
    # async def spotify_current_song(self, ctx) -> None:
    #     if botDB.checkIfAlreadyInserted(ctx.channel.name):
    #         current_song = spotify_playing.get_song(ctx.channel.name, ctx.channel)
    #         await ctx.channel.send(current_song)
    #     else:
    #         await ctx.channel.send(
    #             "It seems that this channel has not yet linked their spotify, please check with the "
    #             "broadcaster."
    #         )

    # @commands.command(name="spotify")
    # async def spotify_token(self, ctx) -> None:
    #     await ctx.channel.send(
    #         "You can sign up here :) -> https://accounts.spotify.com/authorize?client_id"
    #         "=90082084b6b6423f8f08dd85e74f42b4&response_type=code&redirect_uri=https://b816-103-219-21"
    #         "-123.eu.ngrok.io/&scope=user-read-currently-playing"
    #     )


    @commands.command(name="checkKey")
    async def checkSpotifyToken(self, ctx) -> None:
        await ctx.channel.send(botDB.checkSpotifyRefreshToken(ctx.author.name))


    @commands.command(name="sendmsg")
    async def send_message(self):
        for channel in self.connected_channels:
            if channel.name == "ws_zoomers":
                await channel.send("!f")

    # get chatter colour
    # TODO: check if user is in chat, scrape, otherwise resort to API calls
    @commands.command(name="colour")
    async def get_chatter_colour(self, ctx, *, msg):
        user = await self.fetch_users(names=[f"{msg}"])
        user_id = int(user[0].id)
        channel = await self.fetch_chatters_colors([user_id])
        color = str(channel[0].color)
        await ctx.channel.send(color)

    @commands.command(name="sayfile")
    async def sayfile(self, ctx, *, msg) -> None:
        paste_code = msg.split("/")
        paste_code = paste_code[-1]
        print(paste_code)
        login = requests.post("https://pastebin.com/api/api_login.php",
                              data={"api_dev_key": os.environ["PASTEBIN_API_KEY"],
                                    "api_user_name": os.environ["PASTEBIN_USERNAME"],
                                    "api_user_password": os.environ["PASTEBIN_PASSWORD"]})
        print(login)
        response = requests.post("https://pastebin.com/api/api_raw.php",
                                 data={"api_dev_key": str(os.environ["PASTEBIN_API_KEY"]), "api_user_key": login.text,
                                       "api_option": "show_paste", "api_paste_key": paste_code})
        response = response.text.split("\n")
        for line in response:
            await ctx.channel.send(line)
            await asyncio.sleep(0.3)

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
            await asyncio.sleep(0.1)
            column += new[0] + " "
            if len(column) > 500:
                await ctx.channel.send("Message is longer than 500 characters")
                return
            await ctx.channel.send(column)
        column = column.rsplit(" ", 1)[0]

        for row in range(x - 1, 0, -1):
            await asyncio.sleep(0.1)
            column = column.rsplit(" ", 1)[0]
            await ctx.channel.send(column)

    @commands.command(name="r")
    async def randd(self, ctx, *, msg="None") -> None:
        number = randint(1, 3)
        await ctx.channel.send(str(number))

    @commands.command()
    async def dia(self, ctx, *, msg) -> None:
        if str(ctx.author.name) == "themythh":
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
                lat = coords[0]["lat"]
                lon = coords[0]["lon"]
            else:
                await ctx.channel.send(
                    "Please enter a city, or set your location with !set_location"
                )
                return
        # check if list is empty
        if not coords:
            coords = self.get_city_coords(msg)
            if coords == "Could not find city":
                await ctx.channel.send(
                    "Couldn't get city coordinates. Please check spelling and try again."
                )
                return
            lat = coords[0]
            lon = coords[1]
            print(lat)
            print(lon)
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid="
            f"{os.environ['OPENWEATHERMAP_API_KEY']}&units=metric"
        )
        if response.status_code == 404:
            await ctx.channel.send("City not found")
            return

        response = response.json()
        emoji_icon = self.emoji_choice(response["weather"][0]["description"])
        wind_direction = self.deg_to_cardinal(response["wind"]["deg"])
        # convert sunrise and sunset to city's timezone
        try:
            weather = (
                    f"{ctx.author.name}, {response['name']},{response['sys']['country']} (now):"
                    + f" {response['weather'][0]['description']} {emoji_icon}, {response['main']['temp']}ºC ({round(response['main']['temp'] * 1.8 + 32, 2)} ºF), feels like "
                    + f"{response['main']['feels_like']}ºC, Cloud cover: {response['clouds']['all']}%,Wind: {wind_direction} "
                    + f"{response['wind']['speed']}m/s. Humidity: {response['main']['humidity']}%,"
                    + f" Pressure: {response['main']['pressure']}hPa, Sunrise: {self.unix_to_time(response['sys']['sunrise'], response['timezone'])}, "
                    + f" Sunset: {self.unix_to_time(response['sys']['sunset'], response['timezone'])}"
            )
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
    @commands.command(name="set_location", aliases=["sl"])
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
            return emoji.emojize(":cloud_with_rain:", language="alias")
        elif desc == "thunderstorm":
            return emoji.emojize(":cloud_with_lightning_and_rain:", language="alias")
        elif desc == "snow":
            return emoji.emojize(":snowflake:", language="alias")
        elif desc == "mist":
            return emoji.emojize(":fog:", language="alias")
        elif desc == "overcast clouds":
            return emoji.emojize(":cloud:", language="alias")
        else:
            return emoji.emojize(":sunny:", language="alias")

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
        berry = requests.get(self.pokemonClient.get_berry(msg).item.url).json()[
            "effect_entries"
        ]
        for key in range(0, len(berry)):
            if berry[key]["language"]["name"] == "en":
                await ctx.channel.send(berry[key]["short_effect"])
                return

    # def is_trusted_user(self, username) -> bool:
    #     if not self.trusted_users:
    #         self.trusted_users = botDB.get_trusted_users()
    #     for user in self.trusted_users:
    #         if username == user["username"]:
    #             return True
    #     return False

    def is_trusted_user(self, username=None) -> bool:
        return True

    async def event_command_error(
            self, ctx: commands.Context, error: Exception
    ) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            time = str(error).split(".", 1)[1].replace("(", "").replace(")", "")
            await ctx.send("Command is on CD, " + time)

    # command to get a word definition from dictionaryapi
    @commands.command(name="define", aliases=["d"])
    async def define(self, ctx: commands.Context, *, msg) -> None:
        if msg is None:
            await ctx.channel.send("Please enter a word")
            return
        try:
            response = requests.get(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{msg}"
            ).json()
            if response is None:
                await ctx.channel.send("Word not found")
                return
            print(type(response))
            pprint(response)
            await ctx.channel.send(
                response[0]["meanings"][0]["definitions"][0]["definition"])
        except Exception as e:
            print(e)
            await ctx.channel.send("An error has occurred!")

    @commands.command(name="color")
    async def color(self, ctx: commands.Context, *, msg):
        chatters = requests.get(
            f"https://tmi.twitch.tv/group/user/{ctx.channel.name}/chatters"
        ).json()["chatters"]
        print(chatters)
        chatters2 = ctx.channel.chatters
        print(chatters2)
        for chatter in chatters2:
            if chatter.name.lower() == msg.lower():
                chatter2 = ctx.channel.get_chatter(msg)
                print(chatter.name, chatter.color)
                print(chatter2.name, chatter2.color)

    # when was a user last seen.
    @commands.command(aliases=["ls"])
    async def last_seen(self, ctx: commands.Context, *, msg) -> None:
        result = await botDB.get_user(msg)
        result = str(result[0]['last_seen']).split(".")[0]
        await ctx.channel.send(f"{msg} was last seen on {result}")

    # when was a user first seen
    @commands.command(aliases=["fs"])
    async def first_seen(self, ctx: commands.Context, *, msg) -> None:
        result = await botDB.get_user(msg)
        result = str(result[0]['first_seen']).split(".")[0]
        await ctx.channel.send(f"{msg} was first seen on {result}")

    # send message to user when they next speak in chat
    @commands.command(aliases=["remind"])
    async def reminder(self, ctx: commands.Context, *, msg) -> None:
        msg = msg.split(" ")
        user = msg[0]
        for word in msg:
            reminder = " ".join(msg[1:])
        self.reminders.append({'sender': f"{ctx.author.name}", 'for': f"{user}", 'message': f"{reminder}"})
        print(self.reminders)
        await ctx.channel.send(f"I will remind {msg[0]} next time they speak")

    @commands.command(aliases=["e"])
    async def emote(self, ctx: commands.Context, *, msg=None) -> None:
        await ctx.channel.send(emoji.emojize(":fog:"))

    # return pokemon's stats as a message
    @commands.command(aliases=["s"])
    async def stats(self, ctx: commands.Context, *, msg=None) -> None:
        if msg is None:
            await ctx.channel.send("Please enter a pokemon")
            return
        try:
            pokemon = self.pokemonClient.get_pokemon(msg.lower())
            pokemon_type = pokemon.types[0].type.name
            pokemon_type2 = pokemon.types[1].type.name
            pokemon_stats = pokemon.stats
            pokemon_hp = pokemon_stats[0].base_stat
            pokemon_attack = pokemon_stats[1].base_stat
            pokemon_defense = pokemon_stats[2].base_stat
            pokemon_sp_attack = pokemon_stats[3].base_stat
            pokemon_sp_defense = pokemon_stats[4].base_stat
            pokemon_speed = pokemon_stats[5].base_stat
            pokemon_total = pokemon_hp + pokemon_attack + pokemon_defense + pokemon_sp_attack + pokemon_sp_defense + pokemon_speed
            await ctx.channel.send(
                f"{msg} is a {pokemon_type}/{pokemon_type2} It has {pokemon_hp} hp, {pokemon_attack} attack, {pokemon_defense} defense, {pokemon_sp_attack} special attack, {pokemon_sp_defense} special defense, and {pokemon_speed} speed. total stats:{pokemon_total}.")
        except Exception as e:
            print(e)
            await ctx.channel.send("An error has occurred!")

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
                engine="text-davinci-003",
                temperature=1,
                max_tokens=500,
                frequency_penalty=0,
                presence_penalty=0,
                echo=False
            )
            text = response["choices"][0]["text"]
            text.strip("\n")
            text = text.split(" ")
            answer = ""
            for word in text:
                if len(answer + word) > 500:
                    await asyncio.sleep(0.3)
                    await ctx.channel.send(answer)
                    answer = ""
                print(answer)
                answer += " " + word
        except asyncio.exceptions.TimeoutError as t:
            print(t)
            await ctx.channel.send("OpenAI API timed out")
        except Exception as e:
            print(e)
            await ctx.channel.send("An error has occurred!")

    # return pokemon item as a message
    @commands.command(aliases=["i"])
    async def item(self, ctx: commands.Context, *, msg=None) -> None:
        if msg is None:
            await ctx.channel.send("Please enter an item")
            return
        msg.replace(" ", "-")
        try:
            item = self.pokemonClient.get_item(msg.lower())
            item_name = item.name
            item_effect = item.effect_entries[0].effect
            await ctx.channel.send(
                f"{item_name} {item_effect}")
        except Exception as e:
            print(e)
            await ctx.channel.send("An error has occurred!")
# bot.py
if __name__ == "__main__":
    bot = Bot()
    # bot.pool = bot.loop.run_until_complete(
    #     asyncpg.create_pool(
    #         host="6.tcp.ngrok.io",
    #         port='5432',
    #         user='postgres',
    #         password='M1m4897',
    #         database='postgres'
    #     ))
    bot.run()
