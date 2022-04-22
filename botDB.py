from pymongo import MongoClient
from typing import TypedDict


class UserKey(TypedDict):
    name: str
    refreshToken: str


myclient = MongoClient("mongodb://localhost:27017/")
admin = myclient.admin

botDB = myclient["botDatabase"]
chatUsers = botDB["users"]
serverStatusResult = admin.command("serverStatus")
botQuotes = botDB["quotes"]
spotifyTokens = botDB["spotifyRefreshTokens"]


# pprint(serverStatusResult)

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

def setDeathMsg(my_string):
    my_query = my_string
    botQuotes.insert({'deathMsg': my_query})


def getRandDeathMsg():
    msg = botDB.quotes.aggregate(
        [{"$sample": {"size": 1}}]
    )
    for obj in msg:
        msg = (obj["deathMsg"])
    return str(msg)


def insertEmote(dict_arg):
    my_query = dict_arg
    chatUsers.insert(my_query)


# def insetSpotifyRefreshToken(channel_name, refresh_token):
#     try:
#         x = spotifyTokens.find({'name': f'{channel_name}'})[0]['name']
#         print(x)
#     except NameError:
#         return NameError.name + "\nAn error has occurred, please try again."
#     else:
#         if x == refresh_token:
#             return "Token already in database"
#         else:
#             spotifyTokens.insert({'name': f'{channel_name}', 'refreshToken': f'{refresh_token}'})
#             return "Token inserted"
def insetSpotifyRefreshToken(channel_name, refresh_token):
    try:
        spotifyTokens.insert({'name': f'{channel_name}', 'refreshToken': f'{refresh_token}'})
    except Exception as e:
        print(e)
        return "An error has occurred. Use !checkKey to verify if you already have a key in the database, or try again!"


def checkSpotifyRefreshToken(channel_name):
    try:
        x = spotifyTokens.find({'name': f'{channel_name}'})
        if x[0]['name'] is not None:
            return f"@{channel_name}" + " You have a key in the database."
    except Exception as e:
        print(e)
        return f"@{channel_name}" + " You do not have a key in the database."
