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
    __token = os.getenv('TOKEN')

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        self.__client = discord.Client(intents=intents)
        if DiscordClientWrapper.__token == None:
            print("Token not provided")
            # TODO: Send error notification
        else:
            self.__client.run(token=DiscordClientWrapper.__token)

    async def send_message_to_channel(self, channel_id: int, message_text: str) -> Optional[int]:
        try:
            channel = self.__client.get_channel(channel_id)
            if channel != None:
                message = await channel.send(message_text)
                return message.id
            else:
                print("Channel does not exist")
                # TODO: Send error notification
        except Exception as e:
            # TODO: send error notification
            print(e)
