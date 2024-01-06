#!/usr/bin/env python3
import asyncio
import time
from pprint import pprint
import asyncpg
import pokepy
import twitchio
import pokebase as pb

import botDB
import datetime
import emoji
import os
import re
import requests
from datetime import datetime
from asyncio import sleep
from random import randint
from pokebase import cache

cache = cache.API_CACHE
# from spellchecker import SpellChecker
# from twitchio import Channel, User, Client
from twitchio.ext import commands, routines

# import spotify_playing

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
    pokemonClient = pokepy.V2Client(cache="in_disk", cache_location="./cache")
    trusted_users: list = []
    initial_extensions: list = ["cogs.pokemon", "cogs.pokedex", "cogs.db"]
    reminders: list = []
    command_states = {}
    """
    Event that is triggered when the bot is ready to start processing events.
    """

    async def event_ready(self) -> None:
        print(f"Logged into {self.connected_channels} | {self.nick}")
        # self.trusted_users = await botDB.get_trusted_users()
        for channel in self.connected_channels:
            print(channel)
            await channel.send("I am online!")
        for cog in self.initial_extensions:
            print(cog)
            self.load_module(cog)
        commands_list = self.commands.keys()
        print(commands_list)

    async def event_message(self, msg) -> None:
        if (
            msg.first
            and msg.channel.name.lower() == self.nick.lower()
            or msg.content.startswith("@thenerdgebot")
        ):
            print("ai_help event_message")
            await self.ai_help(msg)
        """Responds to incoming messages in the Twitch chat.

        Args:
            self: The Twitch chatbot object.
            msg: A Twitch chat message object.

        Returns:
            None

        The function checks for incoming messages and performs several actions based on the message content. It checks for
        reminders set for the user and sends them a reminder message if a reminder is due. It also handles any Twitch chat
        commands and responses, such as timeouts or greetings. The function increments a counter for each incoming message
        and sends the total number of messages received to the chat when the keyword 'messages' is included in a message
        from a specific user.

        """
        if msg.echo:
            return
        for reminder in self.reminders:
            if reminder["for"] == msg.author.name:
                await msg.channel.send(
                    f"@{msg.author.name} reminder from {reminder['sender']}: {reminder['message']}"
                )
                self.reminders.remove(reminder)
        if msg.content.startswith("!"):
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

            if "messages" in msg.content.lower() and msg.author.name == "themythh":
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
                await msg.channel.send(f"/timeout {msg.author.name} 1m")
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
            if (
                "buy" in msg.content
                and "followers" in msg.content
                and "viewers" in msg.content
                and "primes" in msg.content
            ):
                await msg.channel.send(f"/ban {name}")

    @commands.command(name="newmon")
    async def newmon(self, ctx: commands.Context, *, msg=None):
        print(msg)
        if msg is None:
            await ctx.channel.send("Please enter a pokemon name")
        # types = [poke_type.type.name for poke_type in pb.pokemon(msg).types]
        # print(types)

    @commands.command(name="test")
    async def test(self, ctx: commands.Context, *, msg=None) -> None:
        """A test command to check if the bot is functioning properly.

        Args:
            self: The Twitch chatbot object.
            msg: A Twitch chat message object.

        Returns:
            None

        The function simply responds with a message "test passed!" to indicate that the command has been executed
        successfully. It is used to check if the bot is functioning properly.
        """
        print(ctx)
        await ctx.channel.send("test passed!")

    @commands.command(name="vanish")
    async def vanish(self, msg: twitchio.Message) -> None:
        """Timeouts the user who sends the command for 1 second.

        Args:
            self: The Twitch chatbot object.
            msg: A Twitch chat message object.

        Returns:
            None

        The function sends a timeout command to the user who sends the '!vanish' command, putting them in timeout for 1 second.
        """
        if msg.author.name != bot.nick:
            print(f"/timeout {msg.author.name}")
            await msg.channel.send(f"/timeout {msg.author.name} 1s")

    # @commands.command(name="timer")
    # async def timer(self, ctx, *, msg) -> None:
    #     """Starts a timer for a specified duration and sends a notification message when it runs out.
    #
    #     Args:
    #         self: The Twitch chatbot object.
    #         ctx: A Twitch command context object.
    #         msg: A string message containing the duration for the timer.
    #
    #     Returns:
    #         None
    #
    #     The function takes a string message containing the duration for the timer in seconds, minutes, or hours
    #     (specified with 's', 'm', or 'h' respectively). It then converts the duration to seconds, starts the timer, and
    #     sends a notification message when the timer runs out. The notification message includes the original duration of
    #     the timer in hours, minutes, and seconds.
    #     """
    #     time_unit = msg[-1]
    #     msg = msg.rstrip("hms")
    #     if msg:
    #         total_seconds = int(msg)
    #         if time_unit == "m":
    #             total_seconds *= 60
    #         elif time_unit == "h":
    #             total_seconds *= 3600
    #         if total_seconds > 0:
    #             hours, remainder = divmod(total_seconds, 3600)
    #             mins, secs = divmod(remainder, 60)
    #             time_str = f"{hours}h" if hours else ""
    #             time_str += f"{mins}m" if mins else ""
    #             time_str += f"{secs}s" if secs else ""
    #             await ctx.reply(f"Timer {time_str} started :)")
    #             await asyncio.sleep(total_seconds)
    #             await ctx.reply(f"{time_str} timer, just ran out!")

    # @commands.command(name="timer")
    # async def timer(self, ctx, *, msg=None):
    #     if msg.lower() == "start":
    #         await ctx.channel.send("Timer started")
    #         timer_start = datetime.datetime
    #     else if msg.lower() == "stop":
    #         timer_end = time.time()
    #         await ctx.channel.send("Timer stopped" + str(timer_end - timer_start))

    @commands.command(name="lag")
    async def lag(self, msg) -> None:
        if msg.author.name == "themythh":
            while True:
                await sleep(1)
                await msg.channel.send("SourPls LAG THE CHAT SourPls ")

    @commands.command(name="shoutout")
    async def shoutout(self, ctx, *, msg) -> None:
        game = await self.fetch_channel(msg)
        await ctx.channel.send(
            "Yo what are you waiting for, go check out "
            + msg
            + " at www.twitch.tv/"
            + msg
            + "they were last playing"
        )

    # @commands.command(name="dance")
    # async def dance(self, msg) -> None:
    #     if msg.author.name == "themythh":
    #         while True:
    #             await sleep(5)
    #             await msg.channel.send("SourPls")

    # @commands.command(name="brain")
    # async def dance(self, msg) -> None:
    #     if msg.author.name == "themythh":
    #         while True:
    #             await sleep(1)
    #             await msg.channel.send(
    #                 "/me O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee "
    #                 "AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA "
    #             )

    @commands.command(name="coinflip", aliases=["cf"])
    async def coinflip(self, msg) -> None:
        """Simulates a coin flip and sends the result to the chat.

        Args:
            self: The Twitch chatbot object.
            msg: A Twitch chat message object.

        Returns:
            None

        The function generates a random number between 1 and 2 to simulate a coin flip, and sends the result to the chat.
        If the number is 1, the result is HEADS, otherwise the result is TAILS.
        """
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
    async def goto(self, ctx, *, msg) -> None:
        """Joins the specified Twitch channel and sends a notification message to the chat.

        Args:
            self: The Twitch chatbot object.
            ctx: A Twitch command context object.
            msg: A string message containing the name of the Twitch channel to join.

        Returns:
            None

        The function takes a string message containing the name of the Twitch channel to join, and joins the channel using
        the bot's `join_channels` method. It then sends a notification message to the chat confirming that the bot has
        joined the channel.
        """
        channel_name = [msg]
        await bot.join_channels(channel_name)
        await ctx.channel.send(f"Joined channel: {channel_name}")
        print(channel_name)

    # leave current channel
    @commands.command(name="leave", aliases=["l"])
    async def leave(self, ctx: commands.Context):
        """Leaves the current Twitch channel and sends a notification message to the chat.

        Args:
            self: The Twitch chatbot object.
            ctx: A Twitch command context object.

        Returns:
            None

        The function takes a Twitch command context object and uses its `channel` attribute to get the name of the
        current Twitch channel. It then calls the bot's `part_channels` method to leave the channel and sends a
        notification message to the chat confirming that the bot has left the channel.
        """
        await ctx.channel.send("Leaving channel, bye!")
        await self.part_channels([ctx.channel.name])

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

    @commands.command()
    async def bttvemotes(self, ctx, *, msg=None) -> None:
        """Fetches and displays BetterTTV emotes for the specified Twitch channel, or the current channel if none is specified.

        Args:
            self: The Twitch chatbot object.
            ctx: A Twitch command context object.
            msg: A string representing the name of the Twitch channel to fetch BetterTTV emotes for. Defaults to None.

        Returns:
            None

        If `msg` is None, the function fetches BetterTTV emotes for the current Twitch channel using the `channel` attribute
        of the `ctx` object. Otherwise, it fetches the emotes for the specified channel using the `requests` module to send
        an HTTP GET request to the BetterTTV API. It then splits the response text into a list of words and concatenates
        them until the length of the concatenated string exceeds 500 characters or it reaches the end of the list. The
        concatenated string is then sent to the chat using the `ctx` object's `channel` attribute. The function waits for
        2 seconds before sending the next message, in order to avoid rate limiting.
        """
        if msg is None:
            print(msg, ctx.channel.name)
            msg = ctx.channel.name
        emotesString = ""
        counter = 0
        response = requests.get(f"https://decapi.me/bttv/emotes/{msg}")
        fetch = response.text
        fetch = fetch.split(" ")
        for numbers, word in enumerate(fetch):
            if len(emotesString + word) < 500:
                emotesString += f"{word} "
                counter += 1
            if (len(emotesString + word) > 500) or (numbers == len(fetch) - 1):
                await ctx.channel.send(emotesString)
                emotesString = ""
                counter = 0
                await sleep(2)

    @commands.command(name="7tvemotes")
    async def seventvemotes(self, ctx, *, msg=None) -> None:
        """
            Fetches and sends all 7TV emotes for the given user in the chat. If no user is specified, the emotes for the current channel will be sent.

        Args:
        ctx: The context object.
        msg (optional): The name of the user whose 7TV emotes are to be fetched. If None, the emotes for the current channel will be fetched.

        Returns:

        None. The function only sends messages to the chat.
        """
        if msg is None:
            print(msg, ctx.channel.name)
            msg = ctx.channel.name
        emotesString = ""
        counter = 0
        response = requests.get(f"https://api.7tv.app/v2/users/{msg}/emotes")
        fetch = response.json()
        print(fetch)
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
        """
        Fetches and sends all FFZ emotes for the given user in the chat. If no user is specified, the emotes for the current channel will be sent.
        :param ctx:
        :param msg:
        :return: None. The function sends the emotes as a string to the chat.

        """
        emoteString = ""
        if msg is None:
            print(msg, ctx.channel.name)
            msg = ctx.channel.name

        response = requests.get(f"https://api.frankerfacez.com/v1/room/{msg}")
        fetch = response.json()
        for account, id in fetch["sets"].items():
            for emoticon in id["emoticons"]:
                emoteString += str(emoticon["name"] + " ")
        await ctx.channel.send(emoteString)

    def ffzemotes2(self, msg) -> str:
        """
        Fetches and returns all FFZ emotes for the given user in the chat. If no user is specified, the emotes for the current channel will be sent.
        :param msg:
        :return:  None. A string containing the FrankerFaceZ emotes for the specified channel to the chat.
        """
        emoteString = ""
        response = requests.get(f"https://api.frankerfacez.com/v1/room/{msg}")
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
        """
        Gets the colour of a chatter in the chat.
        Parameters:
            - ctx (commands.Context): The context of the command.
            - msg (str): The username of the Twitch user.

        Returns:
            - This function retrieves the color associated with a Twitch user's username in the current channel. The ctx parameter is the context of the command, and msg is the username of the Twitch user. The function uses the fetch_users method of the TwitchIO library to fetch the user's ID, and then passes that ID to the fetch_chatters_colors method to retrieve the user's color. Finally, the function sends the color to the current channel using the send method of the context.
        """
        user = await self.fetch_users(names=[f"{msg}"])
        user_id = int(user[0].id)
        channel = await self.fetch_chatters_colors([user_id])
        color = str(channel[0].color)
        await ctx.channel.send(color)

    @commands.command(name="sayfile")
    async def sayfile(self, ctx, *, msg) -> None:
        """
             Sends the content of a file hosted on pastebin.com to the chat.

        Parameters:
            - ctx (twitchio.Context): The context of the command invocation.
            - msg (str): The URL of the pastebin.com file.

        Returns:
            None. The function sends the content of the file to the chat.
        """
        paste_code = msg.split("/")
        paste_code = paste_code[-1]
        login = requests.post(
            "https://pastebin.com/api/api_login.php",
            data={
                "api_dev_key": os.environ["PASTEBIN_API_KEY"],
                "api_user_name": os.environ["PASTEBIN_USERNAME"],
                "api_user_password": os.environ["PASTEBIN_PASSWORD"],
            },
        )
        response = requests.post(
            "https://pastebin.com/api/api_raw.php",
            data={
                "api_dev_key": str(os.environ["PASTEBIN_API_KEY"]),
                "api_user_key": login.text,
                "api_option": "show_paste",
                "api_paste_key": paste_code,
            },
        )
        response = response.text.split("\n")
        for line in response:
            await ctx.channel.send(line)
            await asyncio.sleep(0.3)

    @commands.command()
    async def pyramid(self, ctx, *, msg) -> None:
        """
        Creates a pyramid of the given character or word with the given height.
        :param ctx:                 The context of the command.
        :param msg:        The message string passed as argument. Should be in the format "<character> <height>".
        :return:                   None. The function sends the pyramid to the chat.
        """
        new = msg.split(" ")
        limit = 48 if ctx.author.is_broadcaster else 5
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

        for _ in range(x):
            await asyncio.sleep(1)
            column += f"{new[0]} "
            if len(column) > 500:
                await ctx.channel.send("Message is longer than 500 characters")
                return
            await ctx.channel.send(column)
        column = column.rsplit(" ", 1)[0]

        for _ in range(x - 1, 0, -1):
            await asyncio.sleep(1)
            column = column.rsplit(" ", 1)[0]
            await ctx.channel.send(column)

    @commands.command(name="r")
    async def randd(self, ctx, *, msg="None") -> None:
        number = randint(1, 3)
        await ctx.channel.send(str(number))

    @commands.command()
    async def dia(self, ctx, *, msg=None) -> None:
        """
        Sends a message to the chat as the bot only if the author is mythh.
        ctx : twitchio.Context
            The context of the command.
        msg : str, optional
            The message to be sent to the chat.
        :return:
        """
        if msg.author.name != "themythh":
            await ctx.channel.send(f"{msg.author.name} omg lmao hilarious")
            return
        if msg is None:
            await ctx.channel.send("Please send a message")
        # response = (await bot.wait_for('message', predicate=lambda m: m.author == ctx.author))
        await ctx.channel.send(msg)

    @commands.command()
    async def fog(self, ctx) -> None:
        await ctx.channel.send(emoji.emojize(":fog:"))

    @commands.command(name="fact")
    async def facts(self, ctx, *, msg=None) -> None:
        """
        This command sends a fact to the chat based on a given category or a random category if none is specified. It uses the "numbersapi" API to retrieve the fact.
        :param ctx: The context in which the command was triggered
        :param msg: A string indicating the category of the fact to be sent, if any.
        :return None: The function sends the fact to the chat.
        """
        if msg is None:
            facts = ["random/math", "random/trivia"]
            number = randint(0, 1)
            await ctx.channel.send(
                requests.get(f"http://numbersapi.com/{facts[number]}").text
            )

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, msg=None) -> None:
        """
        This command sends a random answer to the chat based on a given question. It uses the "8ball" API to retrieve the answer.
        :param ctx: The context in which the command was triggered
        :param msg: A string indicating the question to be answered.
        :return: None. The function sends the answer to the chat.
        """
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
        """
        This function retrieves the current weather data of a location and sends it to the chat.
        :param ctx: commands.Context object representing the invocation context
        :param msg: Optional string argument representing the location to retrieve the weather data from, or None if the user has set their location
        :return: None. If the weather data was successfully retrieved and sent to the chat, or an error message if the weather data could not be retrieved
        """
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
        """
        This function saves the user's location to the database.
        :param ctx:  commands.Context object representing the invocation context
        :param msg:  Optional string argument representing the location to save, or None if the user has set their location
        :return: None. If the location was successfully saved, or an error message if the location could not be saved
        """
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
        """
        This function updates the user's location in the database.
        :param ctx: commands.Context object representing the invocation context
        :param msg: Optional string argument representing the location to save, or None if the user has set their location
        :return: None. The function sends a message to the user's channel with the response from the botDB.update_location() function. If the city entered by the user is not found, the function sends a message to the user's channel saying "City not found".
        """
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
        """
            Fill the chat with the given message repeatedly until the total message length is at least 500 characters.
        :param ctx:  commands.Context object representing the invocation context
        :param msg:  string argument representing the message to fill the chat with
        :return:  None. The function sends a message to the user's channel with the filled message.
        """
        filled = ""
        while len(filled + msg) < 500:
            filled += f"{msg} "
        await ctx.channel.send(filled)

    # add trusted users for link moderation
    @commands.command(name="permit", aliases=["p"])
    async def permit(self, ctx, *, msg) -> None:
        """
        Add a user to the list of trusted users who can use commands that are restricted to moderators, broadcasters, or owners.
        :param ctx:  commands.Context object representing the invocation context
        :param msg:  string argument representing the user to add to the list of trusted users
        :return:  None. The function sends a message to the user's channel with the response from the botDB.add_trusted_user() function.
        """
        if ctx.author.is_broadcaster or ctx.author.is_mod or ctx.author.is_owner:
            # user_id = requests.get(f"https://api.twitch.tv/helix/users?login={msg}").json()["data"][0]["id"]
            if (
                await botDB.add_trusted_user(username=msg)
                and msg not in self.trusted_users
            ):
                self.trusted_users.append(msg.lower())
            await ctx.channel.send(f"{msg} is now a trusted user!")
        else:
            await ctx.channel.send("You are not allowed to use this command!")

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
        """
        This function handles errors that occur during command execution, and specifically handles the case where a command is on cooldown. It sends a message to the channel indicating the remaining cooldown time.
        :param ctx:  commands.Context object representing the invocation context
        :param error:  Exception object representing the error that occurred
        :return:  None. The function sends a message to the user's channel with the remaining cooldown time.
        """
        if isinstance(error, commands.CommandOnCooldown):
            time = str(error).split(".", 1)[1].replace("(", "").replace(")", "")
            await ctx.send(f"Command is on CD, {time}")

    # command to get a word definition from dictionaryapi
    @commands.command(name="define", aliases=["d"])
    async def define(self, ctx: commands.Context, *, msg) -> None:
        """
        Sends the definition of a word to the channel.
        :param ctx:  commands.Context object representing the invocation context
        :param msg:  string argument representing the word to define
        :return:  None. The function sends a message to the user's channel with the definition of the word.
        """
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
                response[0]["meanings"][0]["definitions"][0]["definition"]
            )
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
            if len(users) == 0:
                await ctx.channel.send("No one tried to catch the pokemon 😪")

    @commands.command(name="start")
    async def start(self, ctx: commands.Context) -> None:
        """
        This function starts the bot's broadcast routine.
        :param ctx:  commands.Context object representing the invocation context
        :return:  None. The function sends a message to the user's channel indicating the broadcast has started.
        """
        self.broadcast.start(ctx)

    # when was a user last seen.
    @commands.command(aliases=["ls"])
    async def last_seen(self, ctx: commands.Context, *, msg) -> None:
        """
        Retrieve the last time a user was seen and send a message to the channel with the information.
        :param ctx:  commands.Context object representing the invocation context
        :param msg:  string argument representing the user to check
        :return:  None. The function sends a message to the user's channel with the last time the user was seen.
        """
        result = await botDB.get_user(msg)
        result = str(result[0]["last_seen"]).split(".")[0]
        await ctx.channel.send(f"{msg} was last seen on {result}")

    # when was a user first seen
    @commands.command(aliases=["fs"])
    async def first_seen(self, ctx: commands.Context, *, msg) -> None:
        """
        This function retrieves and displays the first time a user was seen by the bot.
        :param ctx: commands.Context object representing the invocation context
        :param msg: string argument representing the user to check
        :return: None. The function sends a message to the user's channel with the first time the user was seen.
        """
        result = await botDB.get_user(msg)
        result = str(result[0]["first_seen"]).split(".")[0]
        await ctx.channel.send(f"{msg} was first seen on {result}")

    # send message to user when they next speak in chat
    @commands.command(aliases=["remind"])
    async def reminder(self, ctx: commands.Context, *, msg) -> None:
        """
        Sets a reminder for a user to be triggered next time they speak in chat.
        :param ctx: commands.Context object representing the invocation context
        :param msg: string argument representing the user to remind and the message to send
        :return: None. The function sends a message to the user's channel with the reminder.
        """
        msg = msg.split(" ")
        user = msg[0]
        for word in msg:
            reminder = " ".join(msg[1:])
        self.reminders.append(
            {"sender": f"{ctx.author.name}", "for": f"{user}", "message": f"{reminder}"}
        )
        print(self.reminders)
        await ctx.channel.send(f"I will remind {msg[0]} next time they speak")

    @commands.command(aliases=["e"])
    async def emote(self, ctx: commands.Context, *, msg=None) -> None:
        await ctx.channel.send(emoji.emojize(":fog:"))

    # add command to load a specific cog
    @commands.command(name="lm")
    async def load_m(self, ctx: commands.Context, extension: str) -> None:
        """
        Loads a specified extension (a module containing commands). Only trusted users (broadcaster, moderator, owner, or users added by the "permit" command) can use this command.
        :param ctx: commands.Context object representing the invocation context
        :param extension: string argument representing the extension to load
        :return: None. The function sends a message to the user's channel with the result of the command.
        """
        print(extension)
        self.load_module(f"cogs.{extension}")
        await ctx.channel.send(f"Loaded {extension}")

    # add command to unload specific cog
    @commands.command()
    async def unload(self, ctx: commands.Context, extension: str) -> None:
        """
        Unloads a given extension from the bot. Only trusted users (broadcaster, moderator, owner, or users added by the "permit" command) can use this command.
        :param ctx: commands.Context object representing the invocation context
        :param extension: string argument representing the extension to unload
        :return: None. The function sends a message to the user's channel with the result of the command.
        """
        if self.is_trusted_user(ctx.author.name):
            self.unload_module(f"cogs.{extension}")
            await ctx.channel.send(f"Unloaded {extension}")
        else:
            await ctx.channel.send("You are not authorized to use this command")

    @commands.command(name="ai", aliases=["openai"])
    async def ai(self, ctx: commands.Context, *, msg: str) -> None:
        """
        This function is a command for a Twitch chatbot that uses the OpenAI API to generate text based on user input. The function takes in a message as an argument and sends it to the OpenAI API to generate a response. The response is then split into multiple messages and sent back to the user in the Twitch chat.
        :param ctx: the context object of the command invocation
        :param msg: the message that the user inputs as a prompt for the OpenAI API
        :return: None. It sends messages to the Twitch chat instead
        """
        if not self.is_trusted_user(ctx.author.name):
            await ctx.channel.send("You are not allowed to use this command!")
            return
        if msg is None:
            await ctx.channel.send("Please enter a message")
            return
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": msg}],
                    "max_tokens": 500,
                },
            ).json()
            text = response["choices"][0]["message"]["content"].split(" ")
            print(text)
            answer = f"@{ctx.author.name} "
            for word in text:
                if len(answer + word + " ") > 500:
                    await ctx.channel.send(answer)
                    answer = f"@{ctx.author.name} "
                else:
                    answer += f"{word} "
            await ctx.channel.send(answer)
        except asyncio.exceptions.TimeoutError as t:
            print(t)
            await ctx.channel.send("OpenAI API timed out")
        except Exception as e:
            print("error")
            print(e)
            await ctx.channel.send("An error has occurred!")

    # Function to toggle the state of a command for a specific channel
    @commands.command(name="toggle")
    async def toggle(self, ctx, command_name: str):
        for name, command in self.commands.items():
            if hasattr(command.callback, "toggle"):
                await command.callback.toggle(ctx, command_name)

    async def toggle_command(self, ctx: commands.Context, command_name: str):
        print(ctx.channel)
        channel_id = str(ctx.channel)
        if channel_id not in self.command_states:
            self.command_states[channel_id] = {}

        if command_name in self.command_states[channel_id]:
            self.command_states[channel_id][command_name] = not self.command_states[
                channel_id
            ][command_name]
        else:
            self.command_states[channel_id][command_name] = False

        state = (
            "enabled" if self.command_states[channel_id][command_name] else "disabled"
        )
        await ctx.send(f"Command {command_name} is now {state} in this channel.")

    async def before_invoke(self, ctx):
        channel_id = str(ctx.channel.id)
        command_name = ctx.command.name
        if (
            channel_id in self.command_states
            and command_name in self.command_states[channel_id]
            and not self.command_states[channel_id][command_name]
        ):
            await ctx.send(
                f"Sorry, the {command_name} command is currently disabled in this channel."
            )
            raise commands.CommandError(
                f"Command {command_name} is disabled in this channel."
            )

    @commands.command(name="switch")
    async def toggle_command(self, ctx: commands.Context, command_name: str):
        await self.toggle_command(ctx, command_name)

    # TODO: spawn its own bot to handle support uniquely. will try to figure out a way to monitor ratelimits between
    # the two
    @commands.command(name="ai_help", aliases=["openai_help"])
    async def ai_help(self, ctx, *, msg) -> None:
        print("ai_help")
        """
        This function is a command for a Twitch chatbot that uses the OpenAI API to generate text based on user input. The function takes in a message as an argument and sends it to the OpenAI API to generate a response. The response is then split into multiple messages and sent back to the user in the Twitch chat.
        :param ctx: the context object of the command invocation (here it's part of message)
        :param msg: the message that the user inputs as a prompt for the OpenAI API
        :return: None. It sends messages to the Twitch chat instead
        """
        if msg is None:
            await ctx.channel.send("Please enter a message")
            return
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are thenerdgebot, a twitch chatbot with various capabilities, do not provide command description, only the name, unless they ask for a specific command. If you are ever asked about what commands you have, just group them by theme, say pokemon, utility etc.., if they ask for pokemon commands for example, then give a list without explanations of what each command does, if they ask for a specific command then you can give an explanation, keep messages short."
                            + " Here's a list to the commands you have access to: "
                            + """        ability
            Fetches a pokemon \'s ability.
            Usage: !ability
        ai
            Sends a message to ChatGPT
            Usage: !ai \"your prompt\"
        berry
            Fetches a berry\'s ability.
            Usage: !ability \"ability name\"
        bttvemotes
            Fetches\'s a channel\'s bttvemotes, if used without a channel name, fetches the emotes for the channel you\'re using the command in.
            Usage: !bttvemotes
            !bttvemotes \"channel name\"
        coinflip
            Flips a coin.
            Usage: !coinflip
            !cf
        define
            Returns the definition of a word to chat.
            !define \"word\"
        eight_ball
            Shake a digital 8-ball in chat, trust it with all of your life decisions, let it control your life (please do not)
            !8ball \"your question\"
        facts 
            Gives u a random fact, there was something about history, or math or whatever, who cares just do this
            Usage: !fact /dl>
            ffzemotes
                Works the same way bttvemotes works, either return this channel\'s or the channel passed
                Usage: !ffzemotes
                !ffzemotes \"channel name\"
            fill
                you say \"a\" bot says \"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\" (fills till max message length) probably don\'t use it?
                Usage: !fill \"your message\"
            first_seen
                Checks the bot\'s database to see when the user was seen, if ever
                Usage: !fs \"username\"
            get_chatter_colour
                Gets a chatter\'s name\'s colour
                Usage: !c \"username\"
                !color \"username\"
                !colour \"username\"
            item
                Gets a pokemon item\'s effect description
                Usage: !i \"item name\"
                !item \"item name\"
            goto
                Makes the bot try to join a channel, please do not abuse it, if you abuse you i will make the bot ignore you :)
                Usage: !goto \"channel name\"
            last_seen
                The opposite of first seen....
                Usage: !ls \"channel name\"
            begone
                Join.... leave... you get it
                Usage: !begone
                !l
            move
                Gets a pokemon move\'s description
                Usage: !move \"pokemon move name\"
            pokedex
                Gets a list of the pokemon you\'ve caught through the bot, game incoming COPIUM
                Usage: !pokedex
                !pokedex \"username\"
                !pokedex deviation - shows a percentage list spread of pokemon by first letter
                !pokedex reset - if you say yes, it\'s gone, ALL OF IT, i cannot restore it
            pokemon
                catch a mon, should be gone (soon TM)
                Usage: !mon
            pyramid
                I\'ll let you guess what pyramid does
                Usage: !pyramid \"word\" \"max-height\"
            reminder
            reminders
                Send a reminder to a chatter next time they chat :) Be nice, say good morning or good night
                Usage: !reminder \"username\" \"message\"
            set_location
                Save location for weather command
                Usage: !sl \"city name\" if needed you can do City,US (2 letter country code)
            seventvemotes
                ewtv emotes
                Usage: !7tvemotes
                !7tvemotes \"channel name\"
            timer
                The function takes a string message containing the duration for the timer in seconds, minutes, or hours (specified with \'s\', \'m\', or \'h\' respectively).
                Usage: !timer \"number\" \"s/m/h\"
            trade
                Triggers a pokemon trade with another user bot will guide you through messages, auto cancelled if 1 of the participants doesn\'t respond for a while
                Usage: !t \"username\"
                !trade \"username\"
            trigger
                Pokemon evolution conditions
                !trigger \"pokemon name\"
            update_location
                Change your already set location in the db
                Usage: !ul \"city name\" or city,us (2 letter country code)
            weak_type
                Weakness list for certain pokemon
                Usage: !weak \"pokemon name or pokemon id\"
            weather
                Current weather result for your set location, or provided city name
                Usage: !weather
                !weather city or city,us (2 letter country code)
            ww
                Weakness list for given type or types of pokemon
                Usage: !w \"type name\"
                !w \"type name\" \"type name\"
    """,
                        },
                        {"role": "user", "content": msg},
                    ],
                    "max_tokens": 500,
                },
            ).json()
            text = response["choices"][0]["message"]["content"].split(" ")
            print(response)
            answer = f"@{ctx.author.name} "
            for word in text:
                if len(answer + word + " ") > 500:
                    await ctx.channel.send(answer)
                    answer = f"@{ctx.author.name} "
                else:
                    answer += f"{word} "
            await ctx.channel.send(answer)
        except asyncio.exceptions.TimeoutError as t:
            print(t)
            await ctx.channel.send("OpenAI API timed out")
        except Exception as e:
            print("error")
            print(e)
            await ctx.channel.send("An error has occurred!")


# bot.py
if __name__ == "__main__":
    bot = Bot()
    bot.pool = bot.loop.run_until_complete(
        asyncpg.create_pool(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
        )
    )
    bot.run()
