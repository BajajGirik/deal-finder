import re
from typing import List
from utils.url import URLUtils


class TransformerUtils:
    UNSUPPORTED_URL_EXCEPTION_STRING = "Unsupported urls"

    @staticmethod
    def get_price_from_formatted_string(price: str) -> float:
        # Removing thousands separator form price
        price = price.replace(",", "")
        # This can include underscores
        price_without_chars = re.sub(r"[^0-9.]", "", price)
        return float(price_without_chars)

    @staticmethod
    def sanitize_url(url: str) -> str:
        # TODO: remove query params from url
        return url.strip()

    @staticmethod
    def validate_and_sanitize_urls(*args: str) -> List[str]:
        final_urls = []

        for url in args:
            if not URLUtils.is_amazon_url(url) and not URLUtils.is_flipkart_url(url):
                raise Exception(TransformerUtils.UNSUPPORTED_URL_EXCEPTION_STRING)

            final_urls.append(TransformerUtils.sanitize_url(url))

        return final_urls
