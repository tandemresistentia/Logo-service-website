from django.contrib.auth import get_user_model
import json
from celery import shared_task
from django.core.mail import send_mail
from datamagnum import settings
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template import loader
from django.apps import AppConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common
import time
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from fake_useragent import UserAgent, FakeUserAgentError
from django.http import HttpRequest

class Browser:
    def __init__(self):
        try:
            ua = UserAgent()
            self.user_agent = ua.random
        except FakeUserAgentError:
            self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        options = uc.ChromeOptions()

        # options.add_argument("--user-agent=" + self.user_agent)
        self.bot = uc.Chrome(options=options)
        self.bot.delete_all_cookies()
    def getBot(self):
        return self.bot 

class Data():
    def __init__(self,url):
        
        self.url = url
        self.data = Browser().getBot()
        self.data.minimize_window()
        self.data.get(self.url)
        time.sleep(2)

    def datatest(self):
        group = self.data.find_elements(By.CLASS_NAME, "gig-card-layout")[0]
        groupLink = group.find_elements(By.TAG_NAME, "a")[0].get_attribute('href')

        time.sleep(1)
        self.data.get(groupLink)
        self.data.refresh()
        time.sleep(1)

        self.group = self.data.find_elements(By.CLASS_NAME, "package-type")[0]
        self.groupInfo1 = self.data.find_elements(By.CLASS_NAME, "description")[0]
        scones = {}
        for i in range(3):
            scones['type'+str(i)] = self.group.find_elements(By.CLASS_NAME, "type")[i].text
            scones['price'+str(i)] = self.group.find_elements(By.CLASS_NAME, "price")[i].text
            scones['desc'+str(i)] = self.groupInfo1.find_elements(By.TAG_NAME, "td")[i+1].text

        json_string = json.dumps(scones)

        with open('json_data.json', 'w') as outfile:
            outfile.write(json_string)
    

@shared_task(bind=True)
def test(self):
    p1 = Data('https://www.fiverr.com/search/gigs?query=website%20logo&source=toggle_filters&ref_ctx_id=2c74800ccf9235596702ecd2aac3ed4b&search_in=everywhere&search-autocomplete-original-term=website%20logo&filter=auto&ref=delivery_time%3A7%7Cseller_level%3Atop_rated_seller%2Clevel_two_seller%7Cseller_language%3Aen%7Cis_seller_online%3Atrue%7Cpro%3Aany')
    p1.datatest()

