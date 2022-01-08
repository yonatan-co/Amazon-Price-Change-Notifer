from selenium import webdriver
import time
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def get_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")

  driver = webdriver.Chrome(options=options)
  driver.get("https://www.amazon.com/PF-WaterWorks-PF0989-Disposal-Installation/dp/B078H38Q1M/)")
  return driver


def main():
  driver = get_driver()
  old_price = driver.find_element(by='xpath', value='//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')
  print(old_price.text)
  while True:
    current_price = driver.find_element(by='xpath', value='//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')
    if current_price != old_price:
      message = client.messages \
                    .create(
                        body=f"Dear customer, the price of the item you serch for has been changed",
                        from_=os.environ['TWILIO_NUMBER'],
                        to= os.environ['MY_NUMBER']
                    )
      print(f"the message has been sent.")
      current_price = old_price
    else:
      print('the price didnt change')
      time.sleep(15)

print(main())
