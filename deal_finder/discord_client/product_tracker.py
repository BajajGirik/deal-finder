from bson.errors import InvalidId
from discord import Embed
from discord.ext import commands
from database.database import Database
from constants import ERROR_MESSAGES, ERROR_NOTIFICATION_EMAIL_ADDRESSES
from notification import Notification
from utils.transformer import TransformerUtils

database = Database()

class ProductTrackerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def __handle_command_group(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.reply("No subcommand invoked. Please pass correct subcommand along with necessary arguments")

    @commands.group()
    async def product_tracker(self, ctx: commands.Context) -> None:
        await self.__handle_command_group(ctx)

    @product_tracker.command()
    async def list(self, ctx: commands.Context) -> None:
        user_id = ctx.message.author.id
        products = database.product_tracker.find_by_user_id(str(user_id))

        if len(products) == 0:
            await ctx.reply("No products found")
            return

        message = ""

        for product in products:
            id = product["_id"]
            name = product["name"]
            price_threshold = product["price_threshold"]
            message += f"> 🆔 ID:  {id}\n> \n> 📛 Name:  {name}\n> \n> 💰 Price threshold:  {price_threshold}\n> \n> 🔗 URLs:\n"

            for url in product["url"]:
                message += f"> * {url}\n"

            message += "\n\n\n"

        embed = Embed()
        embed.title = "List of products tracked"
        embed.colour = 16711763
        embed.description = message

        await ctx.reply(embed=embed)

    @product_tracker.group()
    async def add(self, ctx: commands.Context) -> None:
        await self.__handle_command_group(ctx)

    @add.command(name="product")
    async def add_product(self, ctx: commands.Context, name: str, price_threshold: float, *args: str) -> None:
        urls = TransformerUtils.validate_and_sanitize_urls(*args)
        user_id = ctx.message.author.id
        channel_id = ctx.message.channel.id

        inserted_id = database.product_tracker.insert(name, price_threshold, urls, str(user_id), str(channel_id))
        await ctx.reply(f"Successfully inserted product with id = {inserted_id}")

    @add.command(name="url")
    async def add_url(self, ctx: commands.Context, product_id: str, url: str) -> None:
        urls = TransformerUtils.validate_and_sanitize_urls(url)
        is_successful = database.product_tracker.insert_url(product_id, urls[0])

        if is_successful:
            await ctx.reply(f"Successfully added url = {urls[0]} to product")
        else:
            await ctx.reply(ERROR_MESSAGES["NO_PRODUCT_FOUND"].format(product_id))

    @product_tracker.group()
    async def update(self, ctx: commands.Context) -> None:
        await self.__handle_command_group(ctx)

    @update.command()
    async def name(self, ctx: commands.Context, product_id: str, name: str) -> None:
        is_successful = database.product_tracker.update_name(product_id, name)
        if is_successful:
            await ctx.reply(f"Successfully updated product name to {name}")
        else:
            await ctx.reply(ERROR_MESSAGES["NO_PRODUCT_FOUND"].format(product_id))

    @update.command()
    async def price_threshold(self, ctx: commands.Context, product_id: str, price_threshold: float) -> None:
        is_successful = database.product_tracker.update_price_threshold(product_id, price_threshold)
        if is_successful:
            await ctx.reply(f"Successfully updated product price_threshold to {price_threshold}")
        else:
            await ctx.reply(ERROR_MESSAGES["NO_PRODUCT_FOUND"].format(product_id))

    @update.command(name="url")
    async def update_url(self, ctx: commands.Context, product_id: str, old_url: str, new_url: str) -> None:
        urls = TransformerUtils.validate_and_sanitize_urls(new_url)
        is_successful = database.product_tracker.update_url(product_id, old_url, urls[0])

        if is_successful:
            await ctx.reply(f"Successfully updated url to {urls[0]}")
        else:
            await ctx.reply("No product/url found")

    @product_tracker.group()
    async def delete(self, ctx: commands.Context) -> None:
        await self.__handle_command_group(ctx)

    @delete.command(name="product")
    async def delete_product(self, ctx: commands.Context, product_id: str) -> None:
        is_successful = database.product_tracker.delete_by_id(product_id)

        if is_successful:
            await ctx.reply("Successfully deleted product tracking info")
        else:
            await ctx.reply(ERROR_MESSAGES["NO_PRODUCT_FOUND"].format(product_id))

    @delete.command(name="url")
    async def delete_url(self, ctx: commands.Context, product_id: str, url: str) -> None:
        is_successful = database.product_tracker.delete_url(product_id, url)

        if is_successful:
            await ctx.reply(f"Successfully deleted url = {url} from product")
        else:
            await ctx.reply(ERROR_MESSAGES["NO_PRODUCT_FOUND"].format(product_id))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        print(error)

        if isinstance(error.__cause__, InvalidId):
            await ctx.reply("Invalid product id passed. Please try again")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(ERROR_MESSAGES["MISSING_ARGUMENTS"])
            return

        if str(error.__cause__) == TransformerUtils.UNSUPPORTED_URL_EXCEPTION_STRING:
            await ctx.reply("Only amazon or flipkart URLs are allowed currently")
            return

        notification = Notification()
        notification.email.send_email(str(error), "[Error] Discord Command", ERROR_NOTIFICATION_EMAIL_ADDRESSES)

        await ctx.reply("Something went wrong")
