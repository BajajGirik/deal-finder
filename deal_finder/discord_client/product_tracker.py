from bson.errors import InvalidId
from discord.ext import commands
from database.database import Database
from utils.transformer import TransformerUtils

database = Database()

class ProductTrackerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def product_tracker(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.reply('Invalid command passed...')

    @product_tracker.command()
    async def list(self, ctx: commands.Context) -> None:
        user_id = ctx.message.author.id
        products = database.product_tracker.find_by_user_id(str(user_id))

        if len(products) == 0:
            await ctx.reply("No products found")
            return

        message = f"List of products tracked:\n"

        for product in products:
            id = product["_id"]
            name = product["name"]
            price_threshold = product["price_threshold"]
            urls = ", ".join(product["url"])
            message += f"* {name}\n  * ID: {id}\n * Price threshold: {price_threshold}\n * URLs: {urls}\n\n"

        message += "Enjoy Tracking!!"

        await ctx.reply(message)

    @product_tracker.command()
    async def add(self, ctx: commands.Context, name: str, price_threshold: float, *args: str) -> None:
        urls = TransformerUtils.validate_and_sanitize_urls(*args)
        user_id = ctx.message.author.id
        channel_id = ctx.message.channel.id

        inserted_id = database.product_tracker.insert(name, price_threshold, urls, str(user_id), str(channel_id))
        await ctx.reply(f"Successfully inserted product with id = {inserted_id}")

    @product_tracker.command()
    async def delete(self, ctx: commands.Context, product_id: str) -> None:
        is_successful = database.product_tracker.delete_by_id(product_id)

        if is_successful:
            await ctx.reply("Successfully deleted product tracking info")
        else:
            await ctx.reply(f"No product found for id = {product_id}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        print(error)

        if isinstance(error.__cause__, InvalidId):
            await ctx.reply("Invalid product id passed. Please try again")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Missing required parameters.")
            return

        if str(error.__cause__) == TransformerUtils.UNSUPPORTED_URL_EXCEPTION_STRING:
            await ctx.reply("Only amazon or flipkart URLs are allowed currently")
            return

        # TODO: Send email
        await ctx.reply("Something went wrong")
