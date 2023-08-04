import discord
import os
from dotenv import load_dotenv
from discord.ext import tasks
from main import track_all_products

load_dotenv()

# Optional TODO: Can add ping command to get the latest price directly via discord
class DiscordClient(discord.Client):
    async def on_ready(self) -> None:
        print('Logged on as', self.user)
        self.main.start()

    @tasks.loop(minutes=25)
    async def main(self) -> None:
        result = track_all_products()
        for single_result in result:
            channel_id = single_result["inform_on"];
            channel = self.get_channel(channel_id)
            if not channel:
                print(f"Channel with id: {channel_id} not found")
                continue
            message = f"Price Dropped!!!\nURL: {single_result['available_on']}\nPrice: {single_result['lowest_price']}"
            await channel.send(message)

    async def on_message(self, message) -> None:
        print('Message on as', message)

class DiscordClientWrapper:
    @staticmethod
    def run() -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        client = DiscordClient(intents=intents)
        token = os.getenv("TOKEN")
        if not token:
            print("Missing discord token!")
            return

        client.run(token)


DiscordClientWrapper.run()
