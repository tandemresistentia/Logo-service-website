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
        options.add_argument('--headless')
    # options.add_argument("--user-agent=" + self.user_agent)
        self.bot = uc.Chrome(options=options)
        self.bot.delete_all_cookies()
    def getBot(self):
        return self.bot 

class Data():
    def __init__(self,url,number):
        self.url = url
        self.data = Browser().getBot()
        self.data.minimize_window()
        self.data.get(self.url)
        self.number = number
        time.sleep(2)

    def datatest(self):
        
        group = self.data.find_elements(By.CLASS_NAME, "gig-card-layout")[int(self.number)]
        groupLink = group.find_elements(By.TAG_NAME, "a")[0].get_attribute('href')

        time.sleep(1)
        scones = {}
        scones['url'] = groupLink
        self.data.get(groupLink)
        
        self.data.refresh()
        time.sleep(1)

        self.group = self.data.find_elements(By.CLASS_NAME, "package-type")[0]
        self.groupInfo1 = self.data.find_elements(By.CLASS_NAME, "description")[0]
        

        for i in range(3):
            scones['type'+str(i)] = self.group.find_elements(By.CLASS_NAME, "type")[i].text
            price_data = self.group.find_elements(By.CLASS_NAME, "price")[i].text
            price_number = price_data[1:]
            print(price_number)
            try:
                price_number = float(price_number) * 2
            except:
                price_number = int(price_number) * 2

            scones['price'+str(i)] = str(price_number)
            scones['desc'+str(i)] = self.groupInfo1.find_elements(By.TAG_NAME, "td")[i+1].text

        e = 0
        for i in range(21):
            try:
                package_boolean = self.data.find_elements(By.CLASS_NAME, "boolean-pricing-factor")[i]
                try:
                    package_boolean.find_elements(By.CLASS_NAME, "glAQDp5.pricing-factor-check-icon.included")[0]
                    reason = True
                except:
                    reason = False
                if i % 3 == 0 and i!= 0:
                    e+=1

                if reason == True:
                    scones['package_row'+str(i)] = (self.data.find_elements(By.CLASS_NAME, "package-row-label")[e+2]).text
                else:
                    scones['package_row'+str(i)] = ''
            except:
                scones['package_row'+str(i)] = ''
        
        try:
            for o in range(3):
                fake_radio = self.data.find_elements(By.CLASS_NAME, "fake-radio-wrapper")[o]
                scones['package_time'+str(o)] = (fake_radio.find_elements(By.CLASS_NAME, "fake-radio")[0]).text
        except:
            for o in range(3):
                fake_radio = self.data.find_elements(By.CLASS_NAME, "delivery-time")[0]
                scones['package_time'+str(o)] = (fake_radio.find_elements(By.TAG_NAME, "td")[o+1]).text
            
        try:
            revisions_data = self.data.find_elements(By.CLASS_NAME, "revisions-wrapper")[0].text    
            if revisions_data == 'Unlimited Revisions':
                scones['revisions'] = 5
            else:
                scones['revisions'] = revisions_data[:1]
        except:
            scones['revisions'] = 0
        
        json_string = json.dumps(scones)
        with open('json_data'+str(self.number)+'.json', 'w') as outfile:
            outfile.write(json_string)
        self.data.quit()







@shared_task(bind=True)
def test(self):
    for i in range(10):
        print('Works!!')