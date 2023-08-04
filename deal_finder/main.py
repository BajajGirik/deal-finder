from typing import TypedDict, List, Optional
from database  import Database
from database.product_tracker import ProductTrackerModel
from utils import ProductMetaCollector
from notification import Notification

class TrackProductResult(TypedDict):
    lowest_price: float
    available_on: str
    inform_on: int

def track_product(product: ProductTrackerModel) -> Optional[TrackProductResult]:
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

    if not min_price or not min_price_available_on:
        return None

    return TrackProductResult(lowest_price=min_price, available_on=min_price_available_on, inform_on=product["channel_id"])


def track_all_products() -> List[TrackProductResult]:
    products = database.product_tracker.find_all()
    tracked_product_results: List[TrackProductResult] = []

    for product in products:
        result = track_product(product)
        if result:
            tracked_product_results.append(result)

    return tracked_product_results


database = Database()
notification = Notification()
