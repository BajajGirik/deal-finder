from time import sleep
from database  import Database
from constants import INTERNAL_EMAILS
from database.product_tracker import ProductTrackerModel
from utils import ProductMetaCollector
from notification import Notification
import asyncio

database = Database()
notification = Notification()

async def track_product(product: ProductTrackerModel) -> None:
    min_price = None
    min_price_available_on = None

    for url in product["url"]:
        meta = ProductMetaCollector.get_product_meta(url)
        price = meta["price"]
        is_out_of_stock = meta["is_out_of_stock"]

        if is_out_of_stock or price >= product["price_threshold"]:
            continue

        if min_price == None or min_price > price:
            min_price = price
            min_price_available_on = url

    if min_price == None or min_price_available_on == None:
        return

    message = f"Price Dropped!!!\nURL: {min_price_available_on}\nPrice: {min_price}"
    # TODO: Optimisation
    # We can return these promises and await all of them at once rather than
    # blocking the main thread for sending individual notifications
    await notification.discord.send_message_to_channel(product["channel_id"], message)


async def track_all_products() -> None:
    products = database.product_tracker.find_all()
    for product in products:
        await track_product(product)

async def main() -> None:
    while True:
        try:
            await track_all_products()
            sleep(10)
        except Exception as e:
            ## TODO: add better error handling
            notification.email.send_email(str(e), notification.email.DEFAULT_SUBJECT, INTERNAL_EMAILS)


if __name__ == "__main__":
    asyncio.run(main())
