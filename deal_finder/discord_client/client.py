import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from constants import BOT_COMMAND_PREFIX
from discord_client.product_tracker import ProductTrackerCog
from discord_client.tasks import TasksCog

load_dotenv()

# Optional TODO: Can add ping command to get the latest price directly via discord
class DiscordBot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.add_cog(TasksCog(self))
        await self.add_cog(ProductTrackerCog(self))

    async def on_ready(self) -> None:
        print('Logged on as', self.user)


class DiscordWrapper:
    @staticmethod
    def run() -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        bot = DiscordBot(command_prefix=BOT_COMMAND_PREFIX, intents=intents)
        token = os.getenv("TOKEN")
        if not token:
            print("Missing discord token!")
            return

        bot.run(token)
