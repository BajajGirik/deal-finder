from discord.ext import commands
from constants import ADMIN_USER_ID, MAX_PRODUCTS_TRACKED_PER_USER
from database import Database

database = Database()

class DiscordUtils:
    @staticmethod
    async def can_user_track_more_products(ctx: commands.Context) -> bool:
        user_id = str(ctx.message.author.id)
        return user_id == ADMIN_USER_ID or database.product_tracker.count_products_tracked_by_user(user_id) < MAX_PRODUCTS_TRACKED_PER_USER
