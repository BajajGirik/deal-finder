from typing import Optional
import discord
import os
from dotenv import load_dotenv

load_dotenv()

# Optional TODO: Can add ping command to get the latest price directly via discord
class DiscordClient(discord.Client):
    async def on_ready(self) -> None:
        print('Logged on as', self.user)


class DiscordClientWrapper:
    _token = os.getenv('TOKEN')

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        if DiscordClientWrapper._token == None:
            print("Token not provided")
            # TODO: Send error notification
        else:
            self.client.run(token=DiscordClientWrapper._token)

    async def sendMessageToChannel(self, channelId: int, messageText: str) -> Optional[int]:
        try:
            channel = self.client.get_channel(channelId)
            if channel != None:
                message = await channel.send(messageText)
                return message.id
            else:
                print("Channel does not exist")
                # TODO: Send error notification
        except Exception as e:
            # TODO: send error notification
            print(e)
