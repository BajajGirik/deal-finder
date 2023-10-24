import re


class URLUtils:
    @staticmethod
    def __is_complete_match(regex: re.Pattern[str], url: str) -> bool:
        if re.fullmatch(regex, url):
            return True
        return False

    @staticmethod
    def is_valid_url(url: str) -> bool:
        # TODO: Validate the regex string as this was just picked randomly
        valid_url_regex_string = r"(http|https)://(www.)?[]{2,256}\\.[a-z]{2,6}\\b[-a-zA-Z0-9@:%._\\+~#?&//=]*"
        valid_url_regex = re.compile(valid_url_regex_string)

        return URLUtils.__is_complete_match(valid_url_regex, url)

    @staticmethod
    def is_amazon_url(url: str) -> bool:
        amazon_url_regex_string = r"https://www.amazon.in/[a-zA-Z0-9@:%._\\+~#?&//=,-]*"
        amazon_url_regex = re.compile(amazon_url_regex_string)

        return URLUtils.__is_complete_match(amazon_url_regex, url)

    @staticmethod
    def shorten_amazon_url(url):
        product_id_capture_regex = re.compile(r"/dp/([^/]*)")
        match_object = re.search(product_id_capture_regex, url)

        if match_object is None:
            return url
        
        product_id = match_object[1]
        if not product_id:
            return url

        return f"https://www.amazon.in/dp/{product_id}"

    @staticmethod
    def get_url_without_query_params(url):
        return url.split("?")[0]

    @staticmethod
    def is_flipkart_url(url: str) -> bool:
        flipkart_url_regex_string = (
            r"https://www.flipkart.com/[a-zA-Z0-9@:%._\\+~#?&//=,-]*"
        )
        flipkart_url_regex = re.compile(flipkart_url_regex_string)

        return URLUtils.__is_complete_match(flipkart_url_regex, url)
