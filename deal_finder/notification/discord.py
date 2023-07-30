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
    def __init__(self) -> None:
        self.__token = os.getenv('TOKEN') or ""
        if not self.__token:
            raise Exception("Missing discord token")

        intents = discord.Intents.default()
        intents.message_content = True
        self.__client = DiscordClient(intents=intents)

    async def send_message_to_channel(self, channel_id: int, message_text: str) -> Optional[int]:
        if self.__client.is_closed():
            await self.__client.login(token=self.__token)

        channel = self.__client.get_channel(channel_id)
        if not channel:
            raise Exception(f"Channel with id: {channel_id} does not exist")

        message = await channel.send(message_text)
        return message.id
