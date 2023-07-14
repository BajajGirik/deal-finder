from selenium import webdriver
from selenium.webdriver.common.by import By

class Selenium:
    def __init__(self):
        self.__driver =  webdriver.Chrome()

    def goToURL(self,url):
        self.__driver.get(url)

    def findByCssSelector(self, cssSelector):
        try:
            element = self.__driver.find_element(By.CSS_SELECTOR, cssSelector)
            return element.text
        except Exception as e:
            # TODO: Add email notification for error
            return None
