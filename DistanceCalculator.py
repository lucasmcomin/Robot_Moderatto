import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DistanceCalculator:

    def __init__(self):

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        self.nav = webdriver.Chrome(options=options, service=service)
        self.nav.get("https://www.google.com.br/maps")

    def get_distance(self, origem, destino):

        self.nav.find_element('xpath', '//*[@id="searchboxinput"]').send_keys(destino)
        self.nav.find_element('xpath', '//*[@id="searchboxinput"]').send_keys(Keys.ENTER)
        time.sleep(4)
        self.nav.find_element('xpath', '// *[ @ id = "QA0Szd"] / div / div / div[1] / div[2] / div / div[1] / div / div / div[4] / div[1] / button').click()
        time.sleep(2)
        self.nav.find_element('xpath', '// *[ @ id = "sb_ifc50"] / input').send_keys(origem)
        self.nav.find_element('xpath', '// *[ @ id = "sb_ifc50"] / input').send_keys(Keys.ENTER)
        time.sleep(2)
        distance =  self.nav.find_element('xpath', '// *[ @ id = "section-directions-trip-0"] / div[1] / div / div[1] / div[2] / div').text

        return self.__getFloat(distance)


    def __getFloat(self, s):

        r = ""
        for c in s:
            if c != " ":
                if c == ",":
                    c = "."
                r += c
            else:
                break
        return float(r)



    def destroy(self):
        self.nav.close()

