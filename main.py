from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

drive = webdriver.Chrome(options=chrome_options)

drive.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = drive.find_element(By.ID, value="cookie")
items = drive.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

time_out = time.time()
five_min = time.time() + 60 * 5
while True:
    cookie.click()
    if time.time() > time_out:
        all_prices = drive.find_elements(By.CSS_SELECTOR,"#store b")
        item_prices = []
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        money_element = drive.find_element(By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)
        affordable_upgrades = {}
        print(cookie_upgrades.items())
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id
        print(affordable_upgrades)
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        drive.find_element(By.ID, value=to_purchase_id).click()
        timeout = time.time() + 5
        if time.time() > five_min:
            cookie_per_s = drive.find_element(By.ID, value="cps").text
            print(cookie_per_s)
            break
