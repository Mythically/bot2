from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
admin = myclient.admin

botDB = myclient["botDatabase"]
chatUsers = botDB["users"]
serverStatusResult = admin.command("serverStatus")
botQuotes = botDB["quotes"]


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
