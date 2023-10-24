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
    def validate_and_sanitize_urls(*args: str) -> List[str]:
        final_urls = []

        for url in args:
            _url = url.strip()

            if URLUtils.is_amazon_url(_url):
                final_urls.append(URLUtils.shorten_amazon_url(_url))
            elif URLUtils.is_flipkart_url(_url):
                final_urls.append(URLUtils.get_url_without_query_params(_url))
            else:
                raise Exception(TransformerUtils.UNSUPPORTED_URL_EXCEPTION_STRING)

        return final_urls
