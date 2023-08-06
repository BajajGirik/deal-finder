import discord
import os
from dotenv import load_dotenv
from discord.ext import tasks
from constants import ERROR_NOTIFICATION_EMAIL_ADDRESSES
from notification import Notification
from jobs import ProductsTrackerJob

load_dotenv()

# Optional TODO: Can add ping command to get the latest price directly via discord
class DiscordClient(discord.Client):
    async def on_ready(self) -> None:
        print('Logged on as', self.user)
        self.track_products.start()

    @tasks.loop(minutes=10)
    async def track_products(self) -> None:
        result = ProductsTrackerJob.execute()
        for single_result in result:
            channel_id = single_result["channel_id_to_notify"];
            channel = self.get_channel(int(channel_id))
            if not channel:
                print(f"Channel with id: {channel_id} not found")
                continue
            message = f"Price Dropped!!!\nURL: {single_result['available_on']}\nPrice: {single_result['lowest_price']}"
            await channel.send(message)

    @track_products.error
    async def on_error(self, error: BaseException):
        print(error)
        notification = Notification()
        notification.email.send_email(str(error), notification.email.DEFAULT_SUBJECT, ERROR_NOTIFICATION_EMAIL_ADDRESSES)


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
