from time import time
from typing import List, Optional, TypedDict
from database.database import Database
from database.product_tracker import ProductTrackerModel
from utils.product_meta_collector import ProductMetaCollector
from utils.cache import FrequencyCache

database = Database()


class ProductTrackingResult(TypedDict):
    lowest_price: float
    available_on: str
    channel_id_to_notify: str


class ProductsTrackerJob:
    cache: Optional[FrequencyCache] = None

    @staticmethod
    def execute() -> List[ProductTrackingResult]:
        start_time = time()
        ProductsTrackerJob.cache = FrequencyCache()

        products = database.product_tracker.find_all()
        print(f"Tracking total {len(products)} product(s)")

        tracked_product_results: List[ProductTrackingResult] = []

        for product in products:
            result = ProductsTrackerJob.track_product(product)
            if result:
                tracked_product_results.append(result)

        print(f"Found optimial prices for {len(tracked_product_results)} product(s)")

        ProductsTrackerJob.cache = None
        total_time = round(time() - start_time, 2)
        print(
            f"Total time taken to track {len(products)} product(s): {total_time} seconds"
        )
        return tracked_product_results

    @staticmethod
    def track_product(product: ProductTrackerModel) -> Optional[ProductTrackingResult]:
        print(f"Tracking product {product['_id']}", end=": ")
        min_price = None
        min_price_available_on = None

        for url in product["url"]:
            meta = ProductsTrackerJob.cache.get(url)

            if meta is None:
                meta = ProductMetaCollector.get_product_meta(url)
                ProductsTrackerJob.cache.set(url, meta)

            price = meta["price"]
            is_out_of_stock = meta["is_out_of_stock"]

            if is_out_of_stock or price >= product["price_threshold"]:
                continue

            if min_price == None or min_price > price:
                min_price = price
                min_price_available_on = url

        if not min_price or not min_price_available_on:
            print("Unable to find optimal price")
            return None

        print("Found optimal price")
        return ProductTrackingResult(
            lowest_price=min_price,
            available_on=min_price_available_on,
            channel_id_to_notify=product["channel_id"],
        )
