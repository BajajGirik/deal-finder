from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class Selenium:

    def __init__(self):
        self._driver =  webdriver.Chrome()
        self.instance = []

    def goToURL(self,url):
        
        self._driver.get(url)
        self._driver.quit()

    def findByCssSelector(self, url):
        try:
        
            self._driver.get(url)
            element = self._driver.find_element_by_css_selector(url)
            return element.text

        except Exception:
            print("Element not found.")
    
        finally:
            self._driver.quit()
    

