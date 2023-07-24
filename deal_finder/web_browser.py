from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By

class WebBrowser:
    def __init__(self) -> None:
        self.__driver =  webdriver.Chrome()

    def go_to_url(self,url) -> None:
        self.__driver.get(url)

    def get_element_text_by_css_selector(self, css_selector) -> Optional[str]:
        try:
            element = self.__driver.find_element(By.CSS_SELECTOR, css_selector)
            return element.text
        except Exception as e:
            # TODO: Add email notification for error
            return None
