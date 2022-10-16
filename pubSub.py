import twitchio
import asyncio
import os
from twitchio.ext import pubsub

my_token = os.environ["TMI_TOKEN"]
users_oauth_token = os.environ["PUB_SUB_TOKEN"]
users_channel_id = os.environ["PUB_SUB_ID"]
client = twitchio.Client(token=my_token)
client.pubsub = pubsub.PubSubPool(client)


@client.event()
async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
    print("bits redemption" + str(event))
    chan = client.get_channel("zack_ko")
    await chan.send("Cheer!")


@client.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    print("channel points" + str(event))
    chan = client.get_channel("zack_ko")
    await chan.send("Points redemption!")


async def main():
    topics = [
        pubsub.channel_points(users_oauth_token)[users_channel_id],
        pubsub.bits(users_oauth_token)[users_channel_id],
    ]
    await client.pubsub.subscribe_topics(topics)
    await client.start()


if __name__ == "__main__":
    client.loop.run_until_complete(main())
