# import datetime
import asyncio
import logging
import os
import traceback

import asyncpg


# import asyncio
# from pymongo import MongoClient
# import time as t


#
# myclient = MongoClient("mongodb://localhost:27017/")
# admin = myclient.admin
# botDB = myclient["botDatabase"]
# chatUsers = botDB["users"]
# serverStatusResult = admin.command("serverStatus")
# botExampleMons = botDB["exampleMons"]
# spotifyTokens = botDB["spotifyRefreshTokens"]
# botGeneric = botDB['bot']


# create connection to database

# class Database(commands.Cog):
async def connect_to_db():
    conn = await asyncpg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )
    return conn


# def insetSpotifyRefreshToken(channel_name, refresh_token):
#     try:
#         x = spotifyTokens.find({'name': f'{channel_name}'})[0]['name']
# #         print(x)
#     except NameError:
#         return NameError.name + "\nAn error has occurred, please try again."
#     else:
#         if x == refresh_token:
#             return "Token already in database"
#         else:
#             spotifyTokens.insert({'name': f'{channel_name}', 'refreshToken': f'{refresh_token}'})
#             return "Token inserted"

#########################################################
################### USERS MANAGMENT #####################
#########################################################

# get user_id for username using pool connection
# class MyCog(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot
#
#     async def get_user_id(self, username: str) -> int:
#         try:
#             async with bot.pool.acquire() as conn:
#                 return await conn.fetch(
#                     "SELECT user_id FROM users WHERE username = $1", username
#                 )
#         except Exception as e:
#             print(e)


# if username not in database, add it in users postgresql
async def newUser(username: str, user_id: int) -> bool:
    try:
        conn = await connect_to_db()
        if not await conn.fetchval(
                "SELECT exists (SELECT 1 FROM users WHERE user_id = $1 limit 1)", user_id
        ):
            await conn.fetch(
                "INSERT INTO users (username, user_id, messages) VALUES ($1, $2, $3)",
                username,
                user_id,
                1,
            )
        # await conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# get user's info
async def get_user(username: str):
    try:
        conn = await connect_to_db()
        user = conn.fetch(f"SELECT * FROM users WHERE username={username}")
        return user
    except Exception as e:
        print(e)


# if username in database, update messages
async def updateMessages(username: str, user_id: int) -> bool:
    if not await newUser(username, user_id):
        return False
    try:
        conn = await connect_to_db()
        await conn.fetch(
            "UPDATE users SET messages = messages + 1 WHERE username = $1", username
        )
        await conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# check if user_id is in user_locations in postgresql
async def is_location_set(user_id: int) -> bool:
    try:
        conn = await connect_to_db()
        if await conn.fetchval(
                "SELECT exists (SELECT user_id FROM user_locations WHERE user_id = $1 limit 1)",
                user_id,
        ):
            await conn.close()
            return True
        else:
            await conn.close()
            return False
    except Exception as e:
        print(e)
        return False


# set user location in postgresql
async def set_location(user_id: int, city_name: str, lat: int, lon: int, hidden: bool) -> str:
    try:
        conn = await connect_to_db()
        await conn.execute(
            "INSERT INTO user_locations (user_id, city_name, lat, lon, hidden) VALUES "
            "($1, $2, $3, $4, $5)",
            user_id,
            city_name,
            lat,
            lon,
            hidden,
        )
        await conn.close()
        return "Location set!"
    except Exception as e:
        print(e)
        return "Location save failed, if you want to update your location please use !update_location"


# update user's location in postgresql
async def update_location(
        user_id: int, city_name: str, lat: int, lon: int, hidden: bool) -> str:
    try:
        conn = await connect_to_db()
        await conn.fetch(
            "UPDATE user_locations SET city_name = $2, lat = $3, lon = $4, hidden = $5  WHERE user_id = $1",
            user_id,
            city_name,
            lat,
            lon,
            hidden,
        )
        await conn.close()
        return "Updated location!"
    except Exception as e:
        print(e)
        return "An error has occurred, please try again!"


# get user_id's location from postgresql
async def get_location(user_id: int) -> str:
    try:
        conn = await connect_to_db()
        location = await conn.fetch(
            "SELECT * FROM user_locations WHERE user_id = $1", user_id
        )
        await conn.close()
        return location
    except Exception as e:
        logging.error(traceback.format_exc())
        print(e)


# add trusted user to postgresql
async def add_trusted_user(username: str) -> bool:
    try:
        conn = await connect_to_db()
        await conn.fetch(
            "INSERT INTO trusted_users (username) VALUES ($1)",
            username,
        )
        await conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# get trusted users from postgresql
async def get_trusted_users() -> [str]:
    try:
        conn = await connect_to_db()
        trusted_users = await conn.fetch("SELECT username FROM trusted_users")
        await conn.close()
        return trusted_users
    except Exception as e:
        print(e)
        return [0]


# delete trusted user from postgresql
async def delete_trusted_user(username: str) -> bool:
    try:
        conn = await connect_to_db()
        await conn.fetch("DELETE FROM trusted_users WHERE username= $1", username)
        await conn.close()
        return True
    except Exception as e:
        print(e)
        return False


#########################################################
############### SPOTIFY TOKEN MANAGMENT #################
#########################################################

# def checkTokenAge(token_time: float):
#     # print(abs(token_time - t.time()))
#     if abs(token_time - t.time()) < 3540:
#         return True
#     else:
#         return False
#
#
# def fetchToken(channel_name: str, ctx_channel):
#     try:
#         return spotifyTokens.find({'name': f'{channel_name}'})
#     except Exception as e:
#         print(e)
#         return bot.send_message("Error has occurred", ctx_channel)
#
#
# def updateToken(channel_name, refresh_token, ctx_channel):
#     try:
#         # spotifyTokens.find_one_and_update()
#         # print(channel_name, refresh_token)
#         spotifyTokens.update_one({'name': f'{channel_name}'},
#                                  {'$set': {'refreshToken': f'{refresh_token}', 'time': f'{t.time()}'}}, upsert=True)
#     except Exception as e:
#         print(e)
#         return bot.send_message("An error has occurred, please try again!", ctx_channel)
#
#
# def insetSpotifyRefreshToken(channel_name, refresh_token, get_token):
#     if checkIfAlreadyInserted(channel_name):
#         return False
#     try:
#         spotifyTokens.insert({'name': f'{channel_name}', 'refreshToken': f'{refresh_token}', 'getToken': f'{get_token}',
#                               'time': f'{t.time()}'})
#         return True
#     except Exception as e:
#         print(e)
#         return "An error has occurred. Use !checkKey to verify if you already have a key in the database, or try again!"
#
#
# def checkIfAlreadyInserted(channel_name):
#     try:
#         if chatUsers.find_one({"username": channel_name}) is not None:
#             return True
#         else:
#             return False
#     except Exception as e:
#         print(e)
#         return
#
#
# def checkSpotifyRefreshToken(channel_name):
#     try:
#         x = spotifyTokens.find({'name': f'{channel_name}'})
#         if x[0]['name'] is not None:
#             # print(x[0]['refreshToken'])
#             return f"@{channel_name}" + " You have a key in the database."
#     except Exception as e:
#         print(e)
#         return f"@{channel_name}" + " You do not have a key in the database."


#####################################################################
################### POKEMON & BATTLES MANAGMENT #####################
#####################################################################

# insert pokemon into postgresql
async def insertCaughtPokemon(pokemon_id: int, pokemon_name: str, user_id: int, username: str) -> bool:
    try:
        conn = await connect_to_db()
        await conn.fetch(
            "INSERT INTO pokemon (id, user_id, pokemon_name, username) VALUES ($1, $2, $3, $4)",
            pokemon_id,
            user_id,
            pokemon_name,
            username,
        )
        await conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# get random pokemon from example_mons in postgresql
async def getEscapePhrase() -> str:
    try:
        conn = await connect_to_db()
        pokemon = await conn.fetchval(
            "SELECT * FROM example_mons ORDER BY RANDOM() LIMIT 1"
        )
        await conn.close()
        return f"{pokemon} just: dodged your pokeball, laughed at you and hopped away happily"
    except Exception as e:
        print(e)
        return "An error has occurred, please try again!"


# get all caught pokemon for user_id from postgresql
async def getPokedex(username: str) -> str:
    try:
        conn = await connect_to_db()
        pokemon = await conn.fetch(
            "SELECT * FROM pokemon JOIN users u on u.user_id = pokemon.user_id WHERE u.username "
            "= $1 ",
            username,
        )
        await conn.close()
        return pokemon
    except Exception as e:
        print(e)
        return "An error has occurred, please try again!"


# reset pokedex for user_id in postgresql
# async def resetPokedex(username: str) -> str:
#     try:
#         conn = await connect_to_db()
#         await conn.fetch(
#             "DELETE FROM pokemon WHERE user_id = (SELECT user_id FROM users WHERE username = $1)",
#             username,
#         )
#         await conn.close()
#     except Exception as e:
#         print(e)
#         return "An error has occurred, please try again!"


# check if user has caught this pokemon
async def has_caught(user_id: int, mon: str) -> str:
    try:
        conn = await connect_to_db()
        mon = await conn.fetch(f"SELECT pokemon_name FROM pokemon WHERE user_id={user_id} AND pokemon_name={mon}")
        conn.close()
        return mon
    except Exception as e:
        print(e)


# exchange pokemon between two users (user_id and user_id2) (pokemon_name and pokemon_name2) (username and username2)
async def exchange_pokemon(user_id: int, user_id2: int, pokemon_name: str, pokemon_name2: str, username: str,
                           username2: str) -> bool:
    try:
        conn = await connect_to_db()
        await conn.fetch(
            "UPDATE pokemon SET user_id = $1, username = $2 WHERE user_id = $3 AND pokemon_name = $4",
            user_id,
            username,
            user_id2,
            pokemon_name2,
        )
        await conn.fetch(
            "UPDATE pokemon SET user_id = $1, username = $2 WHERE user_id = $3 AND pokemon_name = $4",
            user_id2,
            username2,
            user_id,
            pokemon_name,
        )
        await conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# remove all pokemon from user_id
async def remove_all_pokemon(user_id: int) -> bool:
    try:
        conn = await connect_to_db()
        await conn.fetch(
            "DELETE FROM pokemon WHERE user_id = $1",
            user_id,
        )
        await conn.close()
        return True
    except Exception as e:
        print(e)
        return False
