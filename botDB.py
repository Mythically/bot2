from pymongo import MongoClient
from typing import TypedDict
import time as t

import bot


class UserKey(TypedDict):
    name: str
    refreshToken: str


myclient = MongoClient("mongodb://localhost:27017/")
admin = myclient.admin
botDB = myclient["botDatabase"]
chatUsers = botDB["users"]
serverStatusResult = admin.command("serverStatus")
botExampleMons = botDB["exampleMons"]
spotifyTokens = botDB["spotifyRefreshTokens"]
botGeneric = botDB['bot']

# # pprint(serverStatusResult)

def insert(dict_arg):
    my_query = dict_arg
    chatUsers.insert(my_query)


def dead(my_string):
    my_query = my_string
    chatUsers.find_and_modify(my_query, "False")


# def inc(user):
#     chatUsers.update('_id': user, $inc: {messages, +1})
#     messenger = chatUsers.find('_id': user)
#     messenger.upgade($inc {'messages': +1})

# def setDeathMsg(my_string):
#     my_query = my_string
#     botQuotes.insert({'deathMsg': my_query})
#
#
# def getRandDeathMsg():
#     msg = botDB.quotes.aggregate(
#         [{"$sample": {"size": 1}}]
#     )
#     for obj in msg:
#         msg = (obj["deathMsg"])
#     return str(msg)


def insertEmote(dict_arg):
    my_query = dict_arg
    chatUsers.insert(my_query)


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

def newUser(username):
    # print("checking")
    if chatUsers.find_one({"username": username}) is None:
        # print("none")
        try:
            chatUsers.insert_one({"username": username, "lastSeen": t.time(), "messages": 1})
            return True
        except Exception as e:
            # print(e)
            return False
    return False


async def incMessages(username):
    # print(newUser(username))
    if not newUser(username):
        # print(username)
        chatUsers.update_one({"username": username},
                             {"$set": {"lastSeen": t.time()}})
        chatUsers.update_one({"username": username},
                             {"$inc": {"messages": 1}})


#########################################################
############### SPOTIFY TOKEN MANAGMENT #################
#########################################################

def checkTokenAge(token_time: float):
    # print(abs(token_time - t.time()))
    if abs(token_time - t.time()) < 3540:
        return True
    else:
        return False


def fetchToken(channel_name: str, ctx_channel):
    try:
        return spotifyTokens.find({'name': f'{channel_name}'})
    except Exception as e:
        # print(e)
        return bot.send_message("Error has occurred", ctx_channel)


def updateToken(channel_name, refresh_token, ctx_channel):
    try:
        # spotifyTokens.find_one_and_update()
        # print(channel_name, refresh_token)
        spotifyTokens.update_one({'name': f'{channel_name}'},
                                 {'$set': {'refreshToken': f'{refresh_token}', 'time': f'{t.time()}'}}, upsert=True)
    except Exception as e:
        # print(e)
        return bot.send_message("An error has occurred, please try again!", ctx_channel)


def insetSpotifyRefreshToken(channel_name, refresh_token, get_token):
    if checkIfAlreadyInserted(channel_name):
        return False
    try:
        spotifyTokens.insert({'name': f'{channel_name}', 'refreshToken': f'{refresh_token}', 'getToken': f'{get_token}',
                              'time': f'{t.time()}'})
        return True
    except Exception as e:
        # print(e)
        return "An error has occurred. Use !checkKey to verify if you already have a key in the database, or try again!"


def checkIfAlreadyInserted(chnnel_name):
    try:
        if chatUsers.find_one({"username": chnnel_name}) is not None:
            return True
        else:
            return False
    except Exception as e:
        # print(e)
        return


def checkSpotifyRefreshToken(channel_name):
    try:
        x = spotifyTokens.find({'name': f'{channel_name}'})
        if x[0]['name'] is not None:
            # print(x[0]['refreshToken'])
            return f"@{channel_name}" + " You have a key in the database."
    except Exception as e:
        # print(e)
        return f"@{channel_name}" + " You do not have a key in the database."


#####################################################################
################### POKEMON & BATTLES MANAGMENT #####################
#####################################################################
def getEscapePhrase():
    msg = ""
    mon = botExampleMons.aggregate(
        [{"$sample": {"size": 1}}]
    )
    for thing in mon:
        msg = thing['pokemon']
    phase: str = f'{msg} just: dodged your pokeball, laughed at you and hopped away happily'
    return phase

def insertCaughtPokemon(pokemon_name, username):
    pokemon_name = pokemon_name.capitalize()
    try:
        user = chatUsers.find_one({'username': username})
        if user is not None:
            chatUsers.update_one({'username': username},
                                 {'$addToSet': {'caughtPokemon': {'name': f'{pokemon_name}'}}})
        return "Caught successfully"
    except Exception as e:
        # print(e)
        return "Error occurred"


def getPokedex(username):
    mons = ""
    try:
        if chatUsers.find_one({'username': username}) is not None:
            caught_pokemon = chatUsers.find_one({'username': username})['caughtPokemon']
            # print(len(caught_pokemon))
            # print("lenght ^^^")
            # if len(caught_pokemon) == 0:
            #     return "You have not yet caught a mon, use !mon to catch one!"
            # for pokemon in caught_pokemon:
            #     mons += pokemon
            return caught_pokemon
    except TypeError as e:
        # print("ERROR")
        # print(e)
        return "Are you sure you have caught any mons? Try to catch one with !mon and look at your pokedex again."
    except KeyError as e:
        # print(e)
        return "It seems that you have not caught any pokemon! Try to catch one with !mons"
