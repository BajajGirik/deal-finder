from time import sleep
from typing import TypedDict
from utils.transformer import TransformerUtils
from utils.url import URLUtils
from web_browser import WebBrowser

class ProductMeta(TypedDict):
    price: float
    is_out_of_stock: bool

web_browser = WebBrowser()

class ProductMetaCollector:
    @staticmethod
    def __get_price(css_selector: str) -> float:
        price = web_browser.get_element_text_by_css_selector(css_selector)
        if not price:
            raise Exception("Price not found!")

        return TransformerUtils.get_price_from_formatted_string(price)

    @staticmethod
    def get_product_meta_from_amazon() -> ProductMeta:
        price = ProductMetaCollector.__get_price("#corePriceDisplay_desktop_feature_div .a-offscreen")

        product_availability_text = web_browser.get_element_text_by_css_selector("#availability > span")
        if not product_availability_text:
            # TODO: What happens if this doesn't exist?
            return ProductMeta(price = price, is_out_of_stock=True)

        product_availability_text = product_availability_text.strip()
        is_out_of_stock = "currently unavailable" in product_availability_text.lower()

        return ProductMeta(price=price, is_out_of_stock=is_out_of_stock)


    @staticmethod
    def get_product_meta_from_flipkart() -> ProductMeta:
        price = ProductMetaCollector.__get_price("._30jeq3._16Jk6d")
        is_out_of_stock = web_browser.get_element_text_by_css_selector("._2IVIi8._2Dfasx")
        return ProductMeta(price=price, is_out_of_stock=bool(is_out_of_stock))


    @staticmethod
    def get_product_meta(url: str) -> ProductMeta:
        web_browser.go_to_url(url)
        # This is done so that webpage is able to load up completely before we
        # start accessing text from class names...
        sleep(2)

        if URLUtils.is_amazon_url(url):
            return ProductMetaCollector.get_product_meta_from_amazon()

        elif URLUtils.is_flipkart_url(url):
            return ProductMetaCollector.get_product_meta_from_flipkart()

        else:
            raise Exception(f"URL other than amazon or flipkart not handled: {url}")
