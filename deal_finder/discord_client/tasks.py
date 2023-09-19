from discord.ext import tasks, commands
from constants import ERROR_NOTIFICATION_EMAIL_ADDRESSES
from notification import Notification
from jobs import ProductsTrackerJob


class TasksCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.track_products.start()

    @tasks.loop(minutes=10)
    async def track_products(self) -> None:
        result = ProductsTrackerJob.execute()
        for single_result in result:
            channel_id = single_result["channel_id_to_notify"]
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                print(f"Channel with id: {channel_id} not found")
                continue
            message = f"Price Dropped!!!\nURL: {single_result['available_on']}\nPrice: {single_result['lowest_price']}"
            await channel.send(message)

    @track_products.error
    async def on_error(self, error: BaseException):
        print(error)
        notification = Notification()
        notification.email.send_email(
            str(error),
            notification.email.DEFAULT_SUBJECT,
            ERROR_NOTIFICATION_EMAIL_ADDRESSES,
        )
