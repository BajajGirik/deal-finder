from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class WebBrowser:
    def __init__(self) -> None:
        chrome_options = Options()
        # Run in background without spinning up GUI interface. (Improves efficiency)
        chrome_options.add_argument("--headless")
        # Explicitly bypassing the security level in Docker with --no-sandbox
        # Docker deamon always runs as a root user, Chrome crashes.
        chrome_options.add_argument("--no-sandbox")
        # Explicitly disabling the usage of /dev/shm/. The /dev/shm partition is
        # too small in certain VM environments, causing Chrome to fail or crash.
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Disabling image loading to improve efficiency
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')

        self.__driver =  webdriver.Chrome(options=chrome_options)

    def go_to_url(self,url) -> None:
        self.__driver.get(url)

    def get_element_text_by_css_selector(self, css_selector) -> Optional[str]:
        try:
            element = self.__driver.find_element(By.CSS_SELECTOR, css_selector)
            return element.get_attribute('textContent')
        except Exception as e:
            # TODO: Add email notification for error
            return None
