from typing import List, Optional, TypedDict
from database.database import Database
from database.product_tracker import ProductTrackerModel
from utils.product_meta_collector import ProductMetaCollector
from notification.notification import Notification

database = Database()
notification = Notification()

class ProductTrackingResult(TypedDict):
    lowest_price: float
    available_on: str
    channel_id_to_notify: int

class ProductsTrackerJob:
    @staticmethod
    def execute() -> List[ProductTrackingResult]:
        products = database.product_tracker.find_all()
        tracked_product_results: List[ProductTrackingResult] = []

        for product in products:
            result = ProductsTrackerJob.track_product(product)
            if result:
                tracked_product_results.append(result)

        return tracked_product_results


    @staticmethod
    def track_product(product: ProductTrackerModel) -> Optional[ProductTrackingResult]:
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

        return ProductTrackingResult(lowest_price=min_price, available_on=min_price_available_on, channel_id_to_notify=product["channel_id"])
