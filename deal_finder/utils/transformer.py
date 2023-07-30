import re

class TransformerUtils:
    @staticmethod
    def get_price_from_formatted_string(price: str) -> float:
        # Removing thousands separator form price
        price = price.replace(",", "")
        # This can include underscores
        price_without_chars = re.sub(r"[^0-9.]", "", price)
        return float(price_without_chars)
